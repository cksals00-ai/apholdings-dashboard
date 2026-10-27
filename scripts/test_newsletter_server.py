import copy
import importlib.util
import json
import io
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError


class ServerTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.find_spec('newsletter_server')
        self.assertIsNotNone(spec, 'Hosted newsletter runner has not been implemented')
        import newsletter_server
        self.server = newsletter_server
        self.issue = json.loads((Path(__file__).resolve().parents[1] /
            'site-source/newsletter/issues/2026-10-27.json').read_text())

    def test_retries_transient_failure_but_not_invalid_credentials(self):
        attempts = []
        def operation():
            attempts.append(1)
            if len(attempts) < 3:
                raise HTTPError('https://api.openai.com', 503, 'busy', {}, None)
            return 'done'
        self.assertEqual(self.server.retry(operation, sleep=lambda _: None), 'done')
        self.assertEqual(len(attempts), 3)
        attempts.clear()
        def forbidden():
            attempts.append(1)
            raise HTTPError('https://api.openai.com', 401, 'bad key', {}, None)
        with self.assertRaises(HTTPError):
            self.server.retry(forbidden, sleep=lambda _: None)
        self.assertEqual(len(attempts), 1)

    def test_exhausted_billing_quota_is_reported_without_retrying_or_leaking_body(self):
        for code in ('insufficient_quota', 'credit_balance_exhausted',
                     'organization_spend_limit_exceeded', 'project_spend_limit_exceeded',
                     'organization_usage_limit_exceeded'):
            with self.subTest(code=code):
                attempts = []
                def exhausted(*args, **kwargs):
                    attempts.append(1)
                    body = json.dumps({'error': {'code': code, 'message': 'private account details'}}).encode()
                    raise HTTPError('https://api.openai.com/v1/responses', 429, 'quota', {}, io.BytesIO(body))
                real_retry = self.server.retry
                with patch.object(self.server, 'urlopen', exhausted), \
                     patch.object(self.server, 'retry', lambda operation: real_retry(operation, sleep=lambda _: None)):
                    with self.assertRaises(HTTPError) as caught:
                        self.server.request_json('https://api.openai.com/v1/responses')
                self.assertEqual(getattr(caught.exception, 'api_code', None), code)
                self.assertEqual(len(attempts), 1)

    def test_source_rejects_stale_future_and_impostor_domains(self):
        self.server.check_sources(self.issue, [])
        for url, day in [('https://openai.com.evil.example/news', '2026-10-26'),
                         ('http://openai.com/news', '2026-10-26'),
                         ('https://openai.com/news', '2026-10-28'),
                         ('https://openai.com/news', '2026-10-19')]:
            issue = copy.deepcopy(self.issue)
            issue['stories'][0].update(url=url, published=day)
            with self.assertRaises(ValueError):
                self.server.check_sources(issue, [])

    def test_repeated_source_blocks_generation(self):
        with self.assertRaises(ValueError):
            self.server.check_sources(self.issue, [self.issue['stories'][0]['url']])

    def test_duplicate_candidates_do_not_poison_five_distinct_valid_stories(self):
        self.assertTrue(hasattr(self.server, 'collect_sources'), 'Candidate deduplication is missing')
        candidates = [self.issue['stories'][0], self.issue['stories'][0]] + self.issue['stories'][1:]
        fetched = []
        def fetch(story):
            fetched.append(story['url'])
            return {'url': story['url'], 'body': 'verified original'}
        with patch.object(self.server, 'fetch_source', fetch):
            selected, sources = self.server.collect_sources(candidates, '2026-10-27', [], [])
        self.assertEqual(len(selected), 5)
        self.assertEqual(len(set(fetched)), 5)
        self.assertEqual(len(sources), 5)

    def test_each_fact_and_publication_date_require_independent_support(self):
        rows = [{'url': s['url'], 'supported': True,
                 'publication_date': s['published'], 'reason': 'visible source'}
                for s in self.issue['stories']]
        self.server.check_verdict(self.issue, rows)
        for mutation in ('unsupported', 'date', 'missing', 'duplicate'):
            broken = copy.deepcopy(rows)
            if mutation == 'unsupported': broken[0]['supported'] = False
            if mutation == 'date': broken[0]['publication_date'] = '2026-10-25'
            if mutation == 'missing': broken.pop()
            if mutation == 'duplicate': broken[0] = broken[1]
            with self.assertRaises(ValueError):
                self.server.check_verdict(self.issue, broken)

    def test_published_issue_skips_generation_even_without_api_key(self):
        with patch.object(self.server, 'generate', side_effect=AssertionError('duplicate generation')):
            issue, fresh = self.server.obtain_issue(self.issue['date'])
        self.assertFalse(fresh)
        self.assertEqual(issue['number'], 19)

    def test_existing_registered_issue_is_never_rewritten_or_resent(self):
        existing = {'issue_date': '2026-10-27', 'number': 19, 'status': 'published',
                    'verified': True, 'source_data': self.issue}
        requests = []
        def database(method, route, body=None):
            requests.append(method)
            if method != 'GET': self.fail('Existing edition must not be mutated')
            return [existing]
        with patch.object(self.server, 'database', database), \
             patch.object(self.server, 'verify_public', return_value=True):
            self.assertEqual(self.server.register(self.issue), 'already_registered')
        self.assertEqual(requests, ['GET'])

    def test_public_mismatch_prevents_any_database_write(self):
        with patch.object(self.server, 'verify_public', side_effect=ValueError('PDF mismatch')), \
             patch.object(self.server, 'database', side_effect=AssertionError('unsafe registration')):
            with self.assertRaisesRegex(ValueError, 'mismatch'):
                self.server.register(self.issue)

    def test_early_run_prepares_but_does_not_publish(self):
        self.assertFalse(self.server.publication_due(datetime.fromisoformat('2026-10-27T07:59:59+09:00')))
        self.assertTrue(self.server.publication_due(datetime.fromisoformat('2026-10-27T08:00:00+09:00')))

    def test_checkpoint_roundtrip_is_atomic_and_preserves_completed_stage(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'draft.json'
            self.server.save_json(path, {'stage': 'verified', 'issue': self.issue})
            self.assertEqual(json.loads(path.read_text())['stage'], 'verified')
            self.assertEqual(list(path.parent.glob('*.tmp')), [])

    def test_failed_visual_verdict_cannot_be_reused_as_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pdf = root / 'newsletters/AP-News-2026-10-27.pdf'
            pdf.parent.mkdir()
            pdf.write_bytes(b'pdf fixture')
            folder = root / '.ap-news-state/2026-10-27'
            import hashlib
            fingerprint = hashlib.sha256(pdf.read_bytes() + json.dumps(self.issue, sort_keys=True).encode()).hexdigest()
            self.server.save_json(folder / 'visual-check.json', {'fingerprint': fingerprint, 'passed': False})
            with patch.object(self.server, 'ROOT', root), patch.object(self.server, 'STATE', root / '.ap-news-state'), \
                 patch.object(self.server.subprocess, 'run', side_effect=ValueError('must review again')):
                with self.assertRaisesRegex(ValueError, 'must review again'):
                    self.server.visual_check(self.issue)


if __name__ == '__main__':
    unittest.main()

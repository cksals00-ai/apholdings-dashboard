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
                raise HTTPError('https://example.invalid', 503, 'busy', {}, None)
            return 'done'
        self.assertEqual(self.server.retry(operation, sleep=lambda _: None), 'done')
        self.assertEqual(len(attempts), 3)
        attempts.clear()
        def forbidden():
            attempts.append(1)
            raise HTTPError('https://example.invalid', 401, 'bad key', {}, None)
        with self.assertRaises(HTTPError):
            self.server.retry(forbidden, sleep=lambda _: None)
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

    def test_additional_verified_official_publishers_and_impostors(self):
        for domain in ('oracle.com','microsoft.ai','mitre.org'):
            self.assertEqual(self.server.official_url(f'https://www.{domain}/news'),f'https://www.{domain}/news')
            for url in (f'https://{domain}.evil.example/news',f'https://{domain}@evil.example/news'):
                with self.assertRaises(ValueError):self.server.official_url(url)

    def test_repeated_source_blocks_generation(self):
        with self.assertRaises(ValueError):
            self.server.check_sources(self.issue, [self.issue['stories'][0]['url']])


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



if __name__ == '__main__':
    unittest.main()

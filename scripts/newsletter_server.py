#!/usr/bin/env python3
"""API-free AP News publisher. Accepts locally completed, reviewed documents only.

No API keys, subscriber addresses or delivery payloads are written to disk.
Stages are restartable; registration never updates an existing edition.
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import newsletter as builder

ROOT = builder.ROOT
KST = ZoneInfo('Asia/Seoul')
STATE = ROOT / '.ap-news-state'
SUPABASE = 'https://cgijpcimixaregbpvqbf.supabase.co'
DOMAINS = ('openai.com', 'anthropic.com', 'blog.google', 'deepmind.google',
           'blogs.microsoft.com', 'news.microsoft.com', 'microsoft.com',
           'aws.amazon.com', 'aboutamazon.com', 'blogs.nvidia.com',
           'nvidianews.nvidia.com', 'ai.meta.com', 'about.fb.com', 'huggingface.co',
           'oracle.com', 'microsoft.ai', 'mitre.org', 'claude.com', 'github.blog')
CAPTION = 'AI 제작 · 편집 일러스트 · 실제 제품 화면 아님'


def retry(operation, sleep=time.sleep):
    for attempt in range(4):
        try:
            return operation()
        except (HTTPError, URLError, TimeoutError, ConnectionError) as exc:
            if getattr(exc, 'api_code', '') in (
                    'insufficient_quota', 'billing_hard_limit_reached', 'credit_balance_exhausted',
                    'organization_spend_limit_exceeded', 'project_spend_limit_exceeded',
                    'organization_usage_limit_exceeded'):
                exc.close()
                raise
            if isinstance(exc, HTTPError) and exc.code not in (408, 429, 500, 502, 503, 504):
                exc.close()
                raise
            if attempt == 3:
                raise
            if isinstance(exc, HTTPError):
                exc.close()
            sleep((5, 20, 60)[attempt])


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def load_json(path):
    return json.loads(path.read_text())


def request_json(url, method='GET', body=None, headers=None, timeout=300):
    data = None if body is None else json.dumps(body).encode()
    request = Request(url, data=data, method=method, headers={
        'Content-Type': 'application/json', 'User-Agent': 'AP-News-Publisher/1.0',
        **(headers or {})})
    def send():
        try:
            with urlopen(request, timeout=timeout) as response:
                raw = response.read()
                return json.loads(raw) if raw else None
        except HTTPError as exc:
            # Only a short machine error code is retained, never account details/body.
            try:
                code = json.loads(exc.read(65536)).get('error', {}).get('code')
                if isinstance(code, str) and re.fullmatch(r'[a-zA-Z0-9_-]{1,80}', code):
                    exc.api_code = code
            except (ValueError, AttributeError):
                pass
            raise
    return retry(send)


def official_url(url):
    parsed = urlsplit(url)
    host = parsed.hostname or ''
    if (parsed.scheme != 'https' or parsed.username or parsed.password or
            parsed.port not in (None, 443) or any(c in url for c in '\r\n') or
            not any(host == d or host.endswith('.' + d) for d in DOMAINS)):
        raise ValueError('Non-official or unsafe source URL')
    return url


def check_sources(issue, previous_urls):
    day = date.fromisoformat(issue['date'])
    urls = set(previous_urls)
    for story in issue['stories']:
        official_url(story['url'])
        published = date.fromisoformat(story['published'])
        if not day - timedelta(days=7) <= published <= day:
            raise ValueError('Source is outside the disclosed seven-day limit')
        if story['url'] in urls:
            raise ValueError('Duplicate source from this or an earlier edition')
        urls.add(story['url'])


def check_verdict(issue, rows):
    verdicts = {r['url']: r for r in rows}
    if len(rows) != len(issue['stories']) or len(verdicts) != len(rows):
        raise ValueError('Missing or duplicate source verification')
    for story in issue['stories']:
        row = verdicts.get(story['url'], {})
        if row.get('supported') is not True or row.get('publication_date') != story['published']:
            raise ValueError('Fact or actual announcement date is unsupported')


def wait_for_publication(day, now=lambda: datetime.now(KST), sleep=time.sleep):
    current=now().astimezone(KST)
    target=datetime.combine(date.fromisoformat(day),datetime.min.time(),tzinfo=KST).replace(hour=8)
    if current.date()!=target.date() or (target-current).total_seconds()>5*3600:
        raise ValueError('Reservation must be for today and within five hours of08:00 KST')
    while current<target:
        sleep(min(60,(target-current).total_seconds()))
        current=now().astimezone(KST)
        if current.date()!=target.date():raise ValueError('Reservation date expired')
    print('Publication reservation due; source and duplicate checks still apply',flush=True)


def publication_due(now=None):
    return (now or datetime.now(KST)).astimezone(KST).hour >= 8


def verify_documents(issue):
    from pypdf import PdfReader
    web = html.unescape((ROOT / f'ko/news/daily/{issue["date"]}/index.html').read_text())
    mail = html.unescape((ROOT / f'newsletters/email/{issue["date"]}.html').read_text())
    pdf = PdfReader(ROOT / builder.pdf_path(issue).lstrip('/'))
    compact = lambda text: re.sub(r'\s+', '', text)
    text = compact(''.join(p.extract_text() for p in pdf.pages))
    links = {a.get_object().get('/A', {}).get('/URI') for p in pdf.pages for a in p.get('/Annots', [])}
    if len(pdf.pages) < 2 or '{{unsubscribe_url}}' not in mail:
        raise ValueError('Incomplete PDF or missing unsubscribe placeholder')
    if (pdf.metadata or {}).get('/Title') != f'AP News {issue["date"]} | {issue["title"]}':
        raise ValueError('PDF edition date or title mismatch')
    for key in ('title', 'intro', 'takeaway', 'edition_note'):
        value = issue[key]
        if value not in web or value not in mail or compact(value) not in text:
            raise ValueError(f'Web/email/PDF editorial mismatch: {key}')
    for story in issue['stories']:
        for key in (('title', 'summary', 'fact', 'insight') if issue.get('layout')=='editorial-v2' else ('title', 'summary', 'fact', 'insight', 'action')):
            value = story[key]
            if value not in web or value not in mail or compact(value) not in text:
                raise ValueError(f'Web/email/PDF content mismatch: {key}')
        if story['url'] not in links:
            raise ValueError('PDF original-source link missing')
        if story['image']['path'] not in web or story['image']['path'] not in mail:
            raise ValueError('Shared editorial image missing')
    if issue.get('layout')=='editorial-v2':
        if issue['hero']['path'] not in web or issue['hero']['path'] not in mail:
            raise ValueError('Shared motion cover missing')
        from PIL import Image
        with Image.open(ROOT/issue['hero']['path'].lstrip('/')) as animation:
            if animation.n_frames<2 or animation.info.get('loop')!=0: raise ValueError('Cover must loop')
            for frame in range(animation.n_frames): animation.seek(frame); animation.load()
        with Image.open(ROOT/issue['hero']['poster'].lstrip('/')) as poster: poster.verify()
    return len(pdf.pages)


def verify_public(issue):
    paths = [f'ko/news/daily/{issue["date"]}/index.html',
             builder.pdf_path(issue).lstrip('/'), f'newsletters/email/{issue["date"]}.html']
    paths += [s['image']['path'].lstrip('/') for s in issue['stories']]
    if issue.get('layout')=='editorial-v2': paths += [issue['hero'][key].lstrip('/') for key in ('path','poster')]
    for path in paths:
        url_path = path[:-10] if path.endswith('index.html') else path
        request = Request(builder.ORIGIN + '/' + url_path,
                          headers={'Cache-Control': 'no-cache', 'User-Agent': 'AP-News-Publisher/1.0'})
        def fetch():
            with urlopen(request, timeout=60) as response:
                return response.read()
        if retry(fetch) != (ROOT / path).read_bytes():
            raise ValueError('Public web/PDF/image differs from verified local edition')
    return True


def database(method, route, body=None):
    key = os.environ.get('SUPABASE_SERVICE_KEY')
    if not key:
        raise ValueError('SUPABASE_SERVICE_KEY is missing')
    return request_json(SUPABASE + '/rest/v1/' + route, method, body,
                        {'apikey': key, 'Authorization': 'Bearer ' + key,
                         'Prefer': 'resolution=ignore-duplicates,return=representation'})


def register(issue):
    verify_public(issue)
    route = 'ap_news_issues?' + urlencode({'issue_date': 'eq.' + issue['date'],
                                          'select': 'issue_date,number,status,verified,source_data'})
    existing = database('GET', route)
    if existing:
        row = existing[0]
        if (row['status'] != 'published' or row['verified'] is not True or
                row['number'] != issue['number'] or row['source_data'] != issue):
            raise ValueError('Existing registered edition differs; automatic overwrite prohibited')
        print('Existing edition unchanged; no email resend requested')
        return 'already_registered'
    if issue['date'] != datetime.now(KST).date().isoformat():
        raise ValueError('Do not enqueue an old edition')
    record = {'issue_date': issue['date'], 'number': issue['number'], 'title': issue['title'],
        'status': 'published', 'verified': True, 'source_data': issue,
        'web_url': builder.ORIGIN + builder.page_path(issue),
        'pdf_url': builder.ORIGIN + builder.pdf_path(issue),
        'email_html': (ROOT / f'newsletters/email/{issue["date"]}.html').read_text(),
        'publish_at': issue['date'] + 'T08:00:00+09:00'}
    database('POST', 'ap_news_issues?on_conflict=issue_date', record)
    # Read after ambiguous/duplicate-safe POST; never overwrite a conflicting row.
    saved = database('GET', route)
    if not saved or saved[0]['source_data'] != issue:
        raise ValueError('Registration could not be confirmed')
    print('Edition registered; existing confirmed-subscriber queue will send it')
    return 'registered'


def mail_status(issue):
    rows = database('GET', 'ap_news_deliveries?' + urlencode({
        'issue_date': 'eq.' + issue['date'], 'kind': 'eq.newsletter', 'select': 'state,provider_id'}))
    counts = {}
    for row in rows:
        state = row['state']
        if state == 'sent' and not row.get('provider_id'):
            state = 'unconfirmed'
        counts[state] = counts.get(state, 0) + 1
    print('Mail delivery states (provider acceptance, not inbox confirmation): ' + json.dumps(counts))
    return counts


def wait_mail(day, attempts=None):
    """Read-only queue completion gate; existing scheduler owns all sends."""
    limit = attempts or 120
    for attempt in range(limit):
        state = database('POST', 'rpc/ap_news_delivery_health', {'p_day': day})
        pending = sum(state.get(k, 0) for k in ('pending','processing','retry','failed','uncertain','unconfirmed','eligible_missing'))
        if state.get('accepted',0) >= state['active'] and not pending:
            print('All eligible mail accepted by provider: '+json.dumps(state))
            return state
        if attempts is None:
            limit = min(120, max(20, ((state['active'] + 9) // 10) * 10 + 10))
        if attempt + 1 >= limit: break
        time.sleep(30)
    raise ValueError('Mail provider acceptance incomplete: '+json.dumps(state))


def prepare(day, now=None):
    import newsletter_handoff as handoff
    result = {'day': day, 'due': False, 'state': 'not_due'}
    current=(now or datetime.now(KST)).astimezone(KST)
    if day==current.date().isoformat() and publication_due(current):
        path = builder.ISSUES / f'{day}.json'
        if path.exists() and load_json(path).get('status') == 'published':
            issue = builder.validate_issue(load_json(path))
            verify_documents(issue)
            result.update(due=True, state='already_published')
        else:
            bundle = handoff.download_bundle(day)
            if bundle is None:
                result['state'] = 'awaiting_ready'
                print('::notice::No completed edition for today; no generation or old-edition resend')
            else:
                handoff.install_bundle(bundle, day, ROOT)
                result.update(due=True, state='ready')
    output = os.environ.get('GITHUB_OUTPUT')
    if output:
        with open(output, 'a') as handle:
            handle.write(f'due={str(result["due"]).lower()}\nday={day}\nstate={result["state"]}\n')
    print(json.dumps(result))
    return result


def main():
    parser = argparse.ArgumentParser(description='Publish completed AP News without AI API calls')
    parser.add_argument('stage', choices=['prepare', 'register', 'mail-status', 'verify-ready', 'wait-until-due', 'wait-mail'])
    parser.add_argument('--date', default=datetime.now(KST).date().isoformat())
    args = parser.parse_args()
    date.fromisoformat(args.date)
    if args.stage == 'wait-mail':
        wait_mail(args.date)
    elif args.stage == 'wait-until-due':
        wait_for_publication(args.date)
    elif args.stage == 'prepare':
        prepare(args.date)
    elif args.stage == 'verify-ready':
        import newsletter_handoff as handoff
        bundle = handoff.download_bundle(args.date)
        if bundle is None:
            raise ValueError('Completed bundle was not uploaded')
        issue, _ = handoff.validate_bundle(bundle, args.date)
        print(f'Completed bundle verified: {issue["date"]}; no publication or email requested')
    else:
        issue = builder.validate_issue(load_json(builder.ISSUES / f'{args.date}.json'))
        if args.stage == 'register': register(issue)
        else: mail_status(issue)


if __name__ == '__main__':
    try:
        main()
    except HTTPError as exc:
        print(f'::error::Upstream HTTP {exc.code}', file=sys.stderr)
        sys.exit(1)
    except (ValueError, URLError, TimeoutError) as exc:
        print(f'::error::{str(exc)[:300]}', file=sys.stderr)
        sys.exit(1)

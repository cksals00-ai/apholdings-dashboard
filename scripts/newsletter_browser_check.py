#!/usr/bin/env python3
"""Read-only local rendering checks; subscription requests are intercepted."""
import functools
import http.server
import json
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def main(day):
    folder = ROOT / '.ap-news-state' / day
    folder.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            for width, label in ((390, 'mobile'), (1440, 'desktop')):
                page = browser.new_page(viewport={'width': width, 'height': 1000}, device_scale_factor=1)
                page.route('**/supabase.co/**', lambda route: route.fulfill(
                    content_type='application/json', body=json.dumps({'mail_ready': True})))
                page.goto(f'http://127.0.0.1:{server.server_port}/ko/news/daily/{day}/', wait_until='networkidle')
                page.locator('img').evaluate_all("images => images.forEach(i => i.loading = 'eager')")
                page.evaluate('Promise.all(Array.from(document.images, i => i.decode()))')
                if page.evaluate('document.documentElement.scrollWidth > innerWidth'):
                    raise ValueError('Newsletter overflows viewport')
                if page.locator('.story').count() < 5:
                    raise ValueError('Missing newsletter stories')
                if not page.locator('#reader-email').is_visible():
                    page.locator('#reader-email').scroll_into_view_if_needed()
                if page.locator('input[name=consent]').is_checked():
                    raise ValueError('Subscription consent must be unchecked')
                page.screenshot(path=str(folder / f'{label}.png'), full_page=True)
                page.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    print('Mobile/desktop: all images decoded, no horizontal overflow, consent unchecked')


if __name__ == '__main__':
    main(sys.argv[1])

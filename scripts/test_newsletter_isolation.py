"""Trusted renderer must not import or execute mutable homepage tools."""
import json, os, subprocess, sys, tempfile, unittest
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1]
class IsolationTests(unittest.TestCase):
    def test_homepage_syntax_and_checker_failures_cannot_change_news_renderer(self):
        with tempfile.TemporaryDirectory() as folder:
            site = Path(folder).resolve()
            (site/'scripts').mkdir()
            for name in ('newsletter.py','check_site.py'):
                (site/'scripts'/name).write_text('raise RuntimeError("BROKEN HOMEPAGE TOOL")\n')
            for name in ('site-source','img','ko','newsletters'):
                (site/name).symlink_to(RUNTIME/name,target_is_directory=True)
            env = dict(os.environ, AP_NEWS_SITE_ROOT=str(site), PYTHONPATH=str(RUNTIME/'scripts'))
            code = 'import newsletter as b; import newsletter_server as s; import newsletter_handoff as h; print(b.ROOT); assert b.ROOT == s.ROOT == h.ROOT; assert b.ISSUES == b.ROOT / "site-source/newsletter/issues"; assert "AP News" in b.shell("test","test","/",""); issue=s.load_json(b.ISSUES / "2026-10-30.json"); s.verify_documents(issue)'
            result = subprocess.run([sys.executable,'-c',code],env=env,cwd=site,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(result.stdout.strip(),str(site))
    def test_default_root_is_runtime_checkout(self):
        env = dict(os.environ,PYTHONPATH=str(RUNTIME/'scripts'))
        env.pop('AP_NEWS_SITE_ROOT',None)
        result=subprocess.run([sys.executable,'-c','import newsletter; print(newsletter.ROOT)'],env=env,cwd='/private/tmp' if sys.platform=='darwin' else '/tmp',capture_output=True,text=True,check=True)
        self.assertEqual(result.stdout.strip(),str(RUNTIME))
if __name__=='__main__': unittest.main()

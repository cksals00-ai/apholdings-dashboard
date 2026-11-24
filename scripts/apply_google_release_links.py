#!/usr/bin/env python3
"""Verified Google Play releases, 2026-11-06. Reapply after static generation."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
SAFE='https://play.google.com/store/apps/details?id=com.apholdings.safelist'
MOON='https://play.google.com/store/apps/details?id=com.apholdings.moonshot'
labels={'ko':'Google Play에서 설치','en':'Get it on Google Play','ja':'Google Play でインストール','vi':'Cài đặt trên Google Play','zh-cn':'在 Google Play 安装','fr':'Installer sur Google Play'}
for loc,label in labels.items():
 p=ROOT/loc/'products/safe/index.html'
 if not p.exists(): continue
 s=p.read_text().replace('Android · 추후','Android · Google Play 출시').replace('Android · later','Android · available on Google Play')
 p.write_text(s)
 if SAFE not in s:
  pattern=r'(<div class="actions hero-actions"><a[^>]+href="https://apps.apple.com/kr/app/id6805684034"[^>]*>.*?</a>)(</div>)'
  s,n=re.subn(pattern,lambda m:m[1]+f'<a class="button" href="{SAFE}" target="_blank" rel="noopener noreferrer">{label} ↗</a>'+m[2],s,count=1)
  assert n==1,p
  p.write_text(s)
p=ROOT/'firstinvest/index.html';s=p.read_text()
if MOON not in s:
 banner=f'''<aside id="google-play-release" aria-label="앱 설치 안내" style="max-width:560px;margin:0 auto;padding:12px 16px;background:#fff;color:#1f2421;font:14px/1.6 sans-serif;text-align:center">Android 정식 앱 출시 · <a href="{MOON}" target="_blank" rel="noopener noreferrer" style="color:#21664d;font-weight:700">Google Play에서 구매·설치 ↗</a><br><small>현재 가격은 Google Play에서 확인하세요. 아래 웹 버전도 계속 이용할 수 있습니다.</small></aside>'''
 s,n=re.subn(r'(<body[^>]*>)',lambda m:m[1]+'\n'+banner,s,count=1);assert n==1
 p.write_text(s)
print('Google Play release links applied')

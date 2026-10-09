#!/usr/bin/env python3
"""Single-source AP Daily web, email and branded PDF publishing."""
import json, re, os
from pathlib import Path
from datetime import date
from html import escape
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://www.apholdings.kr'
API = 'https://cgijpcimixaregbpvqbf.supabase.co/functions/v1/ap-news'
ISSUES = ROOT / 'site-source/newsletter/issues'

def validate_issue(issue):
    try:
        day = date.fromisoformat(issue['date'])
        if issue['status'] not in ('draft', 'published') or not isinstance(issue['number'], int) or issue['number'] < 1:
            raise ValueError('Invalid edition status or number')
        for key in ('title','intro','edition_note','takeaway'):
            if not isinstance(issue[key], str) or not issue[key].strip(): raise ValueError(key)
        if issue['status'] == 'published' and issue.get('verified') is not True: raise ValueError('Source verification required')
        if not 5 <= len(issue['stories']) <= 7: raise ValueError('Select 5 to 7 stories')
        urls=set()
        for s in issue['stories']:
            for key in ('title','source','url','published','fact','insight','action'):
                if not isinstance(s[key], str) or not s[key].strip(): raise ValueError(key)
            u=urlsplit(s['url'])
            if u.scheme != 'https' or not u.hostname or u.username or u.password or any(c in s['url'] for c in '\r\n'): raise ValueError('Invalid source URL')
            if s['url'] in urls: raise ValueError('Duplicate source')
            urls.add(s['url'])
            if date.fromisoformat(s['published']) > day: raise ValueError('Source date is in the future')
        return issue
    except (KeyError,TypeError) as exc:
        raise ValueError(f'Missing edition data: {exc}') from exc

def esc(s): return escape(str(s), quote=True)
def pdf_path(i): return f'/newsletters/AP-News-{i["date"]}.pdf'
def page_path(i): return f'/ko/news/daily/{i["date"]}/'
def write(path, text):
    p=ROOT/path.lstrip('/');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')

def subscribe_block():
    return f'''<section class="subscribe" id="subscribe"><div><p class="eyebrow">YOUR DAILY AI PERSPECTIVE</p><h2>좋은 판단은,<br>좋은 소식에서.</h2><p>주요 AI 뉴스와 AP의 관점, 읽기 좋은 PDF까지.<br>매일 오전 8시 발행을 목표로 준비합니다.</p><a class="quiet-link" href="mailto:alfred.park@apholdings.kr?subject=AP%20News%20구독%20문의">구독·제휴 문의 ↗</a></div><form id="subscribe-form" data-api="{API}"><label for="reader-email">이메일 주소</label><input id="reader-email" name="email" type="email" autocomplete="email" maxlength="254" placeholder="you@example.com" required><div class="trap" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div><label class="consent"><input name="consent" type="checkbox" required><span><a href="/ko/news/daily/privacy/">개인정보 수집·이용</a>에 동의하고 AP News 수신을 신청합니다.</span></label><button type="submit">무료 구독 신청 <span aria-hidden="true">→</span></button><p class="form-state" id="subscribe-state" role="status" aria-live="polite">이메일 확인 후 구독이 시작됩니다. 언제든 해지할 수 있습니다.</p></form></section>'''

def shell(title, desc, path, body, noindex=False):
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · AP News</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="{'noindex,follow' if noindex else 'index,follow'}"><meta name="referrer" content="no-referrer"><link rel="canonical" href="{ORIGIN}{path}"><meta property="og:title" content="{esc(title)} · AP News"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{ORIGIN}{path}"><meta property="og:image" content="{ORIGIN}/img/ap_mark.png"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/assets/v2/newsletter.css?v=20261009"><script defer src="/assets/v2/newsletter.js?v=20261009"></script></head><body><a class="skip" href="#main">본문으로 이동</a><header><a class="ap-brand" href="/ko/"><img src="/img/ap_mark.png" width="44" height="22" alt="AP"> <span>AP HOLDINGS</span></a><nav aria-label="뉴스레터 메뉴"><a href="/ko/news/">AP뉴스</a><a href="/ko/news/daily/">지난 호</a><a href="#subscribe">구독 신청</a></nav></header><main id="main">{body}{subscribe_block()}</main><footer><a class="footer-wordmark" href="/ko/news/">AP <i>News</i></a><p>AI 소식을 오늘의 판단으로.<br>발행 AP Holdings · AI 작성 및 원문 확인</p><div><a href="/ko/news/daily/privacy/">개인정보 안내</a><a href="mailto:alfred.park@apholdings.kr">alfred.park@apholdings.kr</a></div><small>© 2026 AP Holdings · Seoul, Korea</small></footer></body></html>'''

def render_issue(i):
    validate_issue(i)
    stories=''.join(f'''<article class="story" id="story-{n}"><div class="story-no">{n:02d}</div><div><p class="eyebrow">{esc(s.get('category','AI NEWS'))}</p><h2>{esc(s['title'])}</h2><p class="source">{esc(s['source'])} · 발표 {esc(s['published'])}</p><p>{esc(s['fact'])}</p><aside><b>AP의 관점</b><p>{esc(s['insight'])}</p></aside><p class="action"><b>오늘 해볼 일</b> {esc(s['action'])}</p><a class="quiet-link" href="{esc(s['url'])}" target="_blank" rel="noopener noreferrer">공식 원문 읽기 ↗</a></div></article>''' for n,s in enumerate(i['stories'],1))
    toc=''.join(f'<a href="#story-{n}"><span>{n:02d}</span>{esc(s["title"])}</a>' for n,s in enumerate(i['stories'],1))
    body=f'''<section class="masthead"><div class="edition">DAILY EDITION · NO. {i['number']:03d}<span>{esc(i['date'].replace('-','.'))}</span></div><p class="name">AP <i>News</i><span>AI & BUSINESS DAILY</span></p><div class="hero"><div><p class="eyebrow">TODAY'S PERSPECTIVE</p><h1>{esc(i['title'])}</h1><p class="lead">{esc(i['intro'])}</p><a class="pdf-link" href="{pdf_path(i)}" download>브랜드 PDF 다운로드 <span>↓</span></a></div><div class="hero-art" aria-hidden="true"><span>Ideas.</span><span>Context.</span><i>Perspective.</i><div class="orbit"></div></div></div><p class="edition-note">{esc(i['edition_note'])}</p></section><div class="reading"><aside class="toc"><p class="eyebrow">IN THIS EDITION</p>{toc}<p>핵심 뉴스 {len(i['stories'])}개<br>약 5분 읽기</p></aside><section class="stories">{stories}<section class="takeaway"><p class="eyebrow">ONE THING TO TAKE AWAY</p><h2>오늘, 하나만 해본다면.</h2><p>{esc(i['takeaway'])}</p></section></section></div><a class="back-link" href="/ko/news/daily/">← 지난 뉴스레터 보기</a>'''
    return shell(i['title'],i['intro'],page_path(i),body,i['status']=='draft')

def render_email(i):
    validate_issue(i)
    rows=''.join(f'''<tr><td style="padding:24px 0;border-bottom:1px solid #ddd5c7"><p style="color:#9b7950;font-size:12px;margin:0 0 10px">{n:02d} · {esc(s['source'])} · {esc(s['published'])}</p><h2 style="font-size:21px;line-height:1.5;margin:0 0 12px">{esc(s['title'])}</h2><p style="font-size:15px;line-height:1.9;margin:0">{esc(s['fact'])}</p><p style="font-size:14px;line-height:1.9;color:#526075"><b>AP의 관점</b> · {esc(s['insight'])}</p><a style="color:#9b7950" href="{esc(s['url'])}">공식 원문 ↗</a></td></tr>''' for n,s in enumerate(i['stories'],1))
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"></head><body style="margin:0;background:#f7f4ed;color:#172338;font-family:Arial,'Apple SD Gothic Neo',sans-serif"><table role="presentation" style="max-width:640px;width:100%;margin:auto;padding:32px 24px"><tr><td><img src="{ORIGIN}/img/ap_mark.png" width="44" style="background:#172338;padding:8px" alt="AP Holdings"><p style="font-size:11px;letter-spacing:2px">DAILY EDITION · NO. {i['number']:03d} · {i['date']}</p><p style="font-size:52px;font-family:Georgia,serif;margin:20px 0">AP <i>News</i></p><h1 style="font-size:28px;line-height:1.5">{esc(i['title'])}</h1><p style="line-height:1.9">{esc(i['intro'])}</p><p><a style="color:#172338" href="{ORIGIN}{page_path(i)}">웹에서 읽기 ↗</a> &nbsp; <a style="color:#9b7950" href="{ORIGIN}{pdf_path(i)}">PDF 다운로드 ↓</a></p></td></tr>{rows}<tr><td style="padding:28px 0"><b>오늘, 하나만 해본다면.</b><p style="line-height:1.9">{esc(i['takeaway'])}</p><p style="font-size:12px;color:#657083;line-height:1.8">{esc(i['edition_note'])}<br>AP Holdings · 문의 alfred.park@apholdings.kr<br>수신을 원하지 않으면 <a href="{{{{unsubscribe_url}}}}">구독 해지</a>를 선택하세요.</p></td></tr></table></body></html>'''

def render_pdf(i):
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.colors import HexColor
    from reportlab.lib.pagesizes import A4
    font_path=Path(os.environ.get('AP_NEWS_FONT',ROOT/'site-source/newsletter/fonts/NotoSansKR-Regular.ttf'))
    if not font_path.exists(): raise RuntimeError(f'Newsletter font missing: {font_path}')
    if 'APKR' not in pdfmetrics.getRegisteredFontNames(): pdfmetrics.registerFont(TTFont('APKR',str(font_path)))
    dest=ROOT/pdf_path(i).lstrip('/');dest.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(dest),pagesize=A4);c.setTitle(f'AP News {i["date"]} | {i["title"]}');c.setAuthor('AP Holdings')
    W,H=A4; M=45; ink='#172338';gold='#9b7950'; muted='#526075'
    style=ParagraphStyle('body',fontName='APKR',fontSize=10.2,leading=18,textColor=HexColor(ink),wordWrap='CJK')
    def p(text,x,y,w=W-2*M,size=10.2,color=ink,leading=None):
        st=ParagraphStyle('p',parent=style,fontSize=size,leading=leading or size*1.75,textColor=HexColor(color))
        para=Paragraph(text,st);_,h=para.wrap(w,H);para.drawOn(c,x,y-h);return y-h
    def base(page):
        c.setFillColor(HexColor('#f7f4ed'));c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(HexColor(ink));c.roundRect(M,H-54,44,28,4,fill=1,stroke=0)
        c.drawImage(str(ROOT/'img/ap_mark.png'),M+4,H-49,width=36,height=18,mask='auto')
        c.setFillColor(HexColor(ink));c.setFont('Helvetica',8);c.drawString(M+48,H-41,'AP HOLDINGS  /  AI & BUSINESS DAILY')
        c.setStrokeColor(HexColor('#ddd5c7'));c.line(M,47,W-M,47)
        c.setFont('Helvetica',8);c.setFillColor(HexColor(muted));c.drawString(M,30,f'AP NEWS  |  {i["date"]}  |  NO. {i["number"]:03d}');c.drawRightString(W-M,30,f'{page:02d}')
    base(1)
    c.setFillColor(HexColor(gold));c.setFont('Helvetica',10);c.drawString(M,H-100,'A DAILY PERSPECTIVE ON AI')
    c.setFillColor(HexColor(ink));c.setFont('Times-Roman',70);c.drawString(M,H-183,'AP');c.setFont('Times-Italic',70);c.drawString(M+115,H-183,'News')
    y=p(esc(i['title']),M,H-225,size=25,leading=38)
    y=p(esc(i['intro']),M,y-22,size=12,color=muted)
    y=p('IN THIS EDITION',M,y-40,size=9,color=gold)
    for n,s in enumerate(i['stories'],1): y=p(f'{n:02d} &nbsp; {esc(s["title"])}',M,y-14,size=11)
    y=p(esc(i['edition_note']),M,90,size=8,color=muted,leading=13)
    if y<52: raise ValueError('PDF cover overflow')
    c.showPage()
    page=2; base(page);y=H-92
    for n,s in enumerate(i['stories'],1):
        # Measure each complete story before drawing, so page breaks never clip it.
        blocks=[(f'{n:02d} · {esc(s.get("category","AI NEWS"))}',9,gold),(esc(s['title']),17,ink),(f'{esc(s["source"])} · 발표 {s["published"]}',8,muted),(esc(s['fact']),10.2,ink),(f'AP의 관점 · {esc(s["insight"])}',10.2,muted),(f'오늘 해볼 일 · {esc(s["action"])}',10.2,ink),(f'<link href="{esc(s["url"])}" color="{gold}">공식 원문 읽기 ↗</link>',9,gold)]
        height=22
        for text,size,color in blocks:
            st=ParagraphStyle('measure',parent=style,fontSize=size,leading=size*1.75)
            height+=Paragraph(text,st).wrap(W-2*M,H)[1]+8
        if y-height<75: c.showPage();page+=1;base(page);y=H-92
        if height>H-170: raise ValueError('Story exceeds one PDF page')
        for text,size,color in blocks: y=p(text,M,y,size=size,color=color)-8
        c.setStrokeColor(HexColor('#ddd5c7'));c.line(M,y,W-M,y);y-=22
    extra=Paragraph(esc(i['takeaway']),style).wrap(W-2*M,H)[1]+95
    if y-extra<75:c.showPage();page+=1;base(page);y=H-92
    y=p('ONE THING TO TAKE AWAY',M,y,size=9,color=gold)
    y=p('오늘, 하나만 해본다면.',M,y-12,size=18)
    y=p(esc(i['takeaway']),M,y-12,size=11)
    if y<65: raise ValueError('PDF final page overflow')
    c.save();return dest

def build_all():
    issues=[]
    for path in sorted(ISSUES.glob('*.json'),reverse=True):
        i=validate_issue(json.loads(path.read_text()))
        if i['status']!='published': continue
        issues.append(i);write(page_path(i)+'index.html',render_issue(i));write(f'/newsletters/email/{i["date"]}.html',render_email(i));render_pdf(i)
    if not issues:return
    newest=issues[0]
    cards=''.join(f'<a class="archive-card" href="{page_path(i)}"><p class="eyebrow">NO. {i["number"]:03d} · {i["date"]}</p><h2>{esc(i["title"])}</h2><p>{esc(i["intro"])}</p><span>읽기 ↗</span></a>' for i in issues)
    write('/ko/news/daily/index.html',shell('AP News Daily','매일 읽는 AI 뉴스와 AP의 관점. 브랜드 PDF와 이메일 구독.','/ko/news/daily/',f'<section class="masthead"><p class="name">AP <i>News</i><span>AI & BUSINESS DAILY</span></p><h1>AI 소식을,<br>오늘의 판단으로.</h1><p class="lead">공식 발표를 선별하고, 우리 일에 필요한 맥락을 더합니다.</p></section><div class="archive-grid">{cards}</div>'))
    privacy='<section class="legal"><p class="eyebrow">AP NEWS · PRIVACY</p><h1>구독 개인정보 안내</h1><p>운영 주체: AP Holdings · 문의 alfred.park@apholdings.kr</p><h2>수집 항목과 목적</h2><p>이메일 주소, 신청 시각, 수신 동의 기록, 이메일 확인·해지 및 발송 상태를 수집합니다. 뉴스레터 발송, 구독 확인, 해지 처리, 발송 오류 대응에 사용합니다. 이름은 입력한 경우에만 보관합니다.</p><h2>보관과 철회</h2><p>구독 중에는 서비스 제공을 위해 보관합니다. 해지하면 즉시 발송 대상에서 제외하고 이메일·동의 기록은 30일 내 삭제합니다. 미확인 신청은 30일 후 삭제합니다. 요청 제한 기록은 7일 내 삭제합니다. 동의는 선택 사항이며, 동의하지 않으면 이메일 구독이 제공되지 않습니다.</p><h2>처리 서비스</h2><p>구독 데이터는 Supabase 서울 리전의 데이터베이스에서 관리하며, 이메일 전송에는 Resend를 사용합니다. 발송 준비를 위해 이메일 주소와 해당 메일 내용이 전송 서비스에 전달될 수 있습니다. 상세한 처리 지역·약관·보관 정책은 각 서비스 안내를 확인할 수 있습니다.</p><p><a href="https://supabase.com/privacy">Supabase 개인정보 안내 ↗</a> · <a href="https://resend.com/legal/privacy-policy">Resend 개인정보 안내 ↗</a></p><h2>문의·열람·삭제</h2><p>이메일의 구독 해지 링크 또는 회사 메일로 요청할 수 있습니다. 처리 과정에서 주소 소유 여부를 확인할 수 있습니다.</p><p>시행일: 2026년 10월 9일</p></section>'
    write('/ko/news/daily/privacy/index.html',shell('구독 개인정보 안내','AP News 구독 개인정보 처리 안내','/ko/news/daily/privacy/',privacy))
    write('/ko/news/daily/manage/index.html',shell('구독 관리','AP News 이메일 확인 및 구독 해지','/ko/news/daily/manage/','<section class="legal"><p class="eyebrow">AP NEWS · SUBSCRIPTION</p><h1>구독 관리</h1><p id="manage-state" role="status">링크를 확인하고 있습니다.</p><button id="manage-action" hidden>확인</button></section>',True))
    promo=f'<section id="apdaily-promo" style="max-width:1240px;margin:36px auto;padding:32px;background:#f7f4ed;border:1px solid #ddd5c7;color:#172338"><p style="font-size:11px;letter-spacing:2px;color:#9b7950">AP NEWS · DAILY EDITION</p><h2 style="font-family:Georgia,serif;font-size:32px;margin:12px 0">AP <i>News Daily</i></h2><p>AI 소식을 오늘의 판단으로. 주요 뉴스·AP의 관점·브랜드 PDF.</p><p><a href="{page_path(newest)}">최신호 읽기 ↗</a> &nbsp; <a href="{pdf_path(newest)}">PDF 다운로드 ↓</a> &nbsp; <a href="/ko/news/daily/#subscribe">무료 구독 신청 →</a></p></section>'
    for lang in ('ko','en','vi','ja','zh-cn','fr'):
        path=ROOT/f'{lang}/news/index.html'
        if not path.exists():continue
        s=path.read_text();s=re.sub(r'<section id="apdaily-promo".*?</section>','',s,flags=re.S)
        block=promo if lang=='ko' else promo.replace('AI 소식을 오늘의 판단으로. 주요 뉴스·AP의 관점·브랜드 PDF.','Daily AI news, AP perspectives and branded PDF. Korean edition.').replace('최신호 읽기','Read the latest').replace('무료 구독 신청','Subscribe').replace('PDF 다운로드','Download PDF')
        s=s.replace('<main id="main">','<main id="main">'+block,1);path.write_text(s)
    write('/newsletters/latest.json',json.dumps({'date':newest['date'],'title':newest['title'],'page':page_path(newest),'pdf':pdf_path(newest)},ensure_ascii=False))
    sm=ROOT/'sitemap.xml'
    if sm.exists():
        text=re.sub(r'<url><loc>[^<]*/news/daily/[^<]*</loc><lastmod>[^<]*</lastmod></url>','',sm.read_text())
        routes=['/ko/news/daily/']+[page_path(i) for i in issues]
        text=text.replace('</urlset>',''.join(f'<url><loc>{ORIGIN}{r}</loc><lastmod>{newest["date"]}</lastmod></url>' for r in routes)+'</urlset>');sm.write_text(text)
    print(f'AP Daily: {len(issues)} editions, web/email/PDF generated')

if __name__=='__main__':build_all()

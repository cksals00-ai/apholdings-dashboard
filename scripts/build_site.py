#!/usr/bin/env python3
"""Dependency-free static generation. Existing domain, asset paths and Pages hosting stay intact."""
from pathlib import Path
from html import escape as e
import json,re
ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'site-source/content.json').read_text())
ORIGIN=CFG['origin']; PUBLISHED=[k for k,v in CFG['locales'].items() if v['status']=='published']
DATA={l:json.loads((ROOT/f'site-source/locales/{l}.json').read_text()) for l in PUBLISHED}
MEDIA=json.loads((ROOT/'site-source/brand-media.json').read_text())
HOME_COPY=json.loads((ROOT/'site-source/home-copy.json').read_text())
SELECT_MEDIA=json.loads((ROOT/'site-source/select-media.json').read_text())
GENERATED=[]
GROUPS=[('decision','Decision Intelligence','From data to clearer action.',['safe','light','revenue','travel']),('commerce','Commerce','From discovery to choice to transaction.',['select','commerce','craft','lia']),('games','Games, Learning & IP','Play. Learn. Create.',['rgrg','cubs','lastwave'])]
FLOWS=['DATA','CONTEXT','DECISION / PROCESS','ACTION','OUTCOME']
ASSETS=['Data','Process','Expert Knowledge','Software','IP','Customer Relationship']
CAPABILITIES=['Commercial Operations','Global Sales','Tourism & International Business','Data Analysis','Product Building','Decision Workflow Design']
MARKET=['Locale','Currency','Timezone','Policy','Evidence','Expert','Marketplace','Payment','Logistics','Partner','Pricing','CS','Terms','Analytics']
POLICIES=[('Safelist','/safelist/privacy.html'),('Hangeul Cubs','/hangeulcubs_privacy.html'),('RGRG','/rgrg/privacy.html'),('IRON GRADE','/irongrade/privacy.html'),('The Other Hours','/theotherhours_privacy.html'),('K-Concert Trip','/kfan_privacy.html'),('나의 첫투자','/privacy.html'),('K-Scan','/kscan/privacy.html'),('Goyo','/goyo/privacy.html')]
def out(path,text):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);GENERATED.append(path)
def c(l,k):return DATA[l]['copy'][k]
def prod(l,pid):return next(x for x in DATA[l]['products'] if x['id']==pid)
def home(l):return f'/{l}/'
def ph(l,pid):return f'/{l}/products/{pid}/'
def link(url,label,cls='text-link',external=False):return f'<a class="{cls}" href="{e(url,quote=True)}"'+(' target="_blank" rel="noopener noreferrer"' if external else '')+f'>{e(label)}</a>'
def button(url,label,primary=False):return link(url,label,'button'+(' primary' if primary else ''))
def flow(items):return '<ol class="flow">'+''.join('<li>'+e(x)+'</li>' for x in items)+'</ol>'
def tags(items):return '<div class="tags">'+''.join('<span>'+e(x)+'</span>' for x in items)+'</div>'
def status(l,key):return f'<span class="status">{e(c(l,key))}</span>'
def mail(subject):
 from urllib.parse import quote
 return 'mailto:'+CFG['contact']+'?subject='+quote('[AP Holdings] '+subject)
def logo(l):return f'<a class="brand" href="{home(l)}" aria-label="AP Holdings home"><span class="brand-mark"><img src="/img/ap_mark.png" alt="" width="29" height="14"></span>AP HOLDINGS</a>'
def head(l,title,description,path,index=True,alternate_suffix=''):
 canonical=ORIGIN+path
 fonts='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&amp;display=swap" rel="stylesheet">' if l=='ko' else ''
 alternates=''.join(f'<link rel="alternate" hreflang="{lang}" href="{ORIGIN}/{lang}/{alternate_suffix}">' for lang in PUBLISHED) if index else ''
 if index:alternates+=f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}/en/{alternate_suffix}">'
 sd={'@context':'https://schema.org','@type':'Organization','name':'AP Holdings','url':ORIGIN,'logo':ORIGIN+'/img/ap_mark.png','description':description,'email':CFG['contact'],'sameAs':['https://www.instagram.com/lia_park55/','https://www.tiktok.com/@lia_park55']}
 return f'''<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(description,quote=True)}"><meta name="robots" content="{'index,follow' if index else 'noindex,follow'}"><link rel="canonical" href="{canonical}">{alternates}<meta property="og:type" content="website"><meta property="og:site_name" content="AP Holdings"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:locale" content="{'ko_KR' if l=='ko' else 'en_US'}"><meta name="theme-color" content="#ffffff"><link rel="icon" href="/img/ap_mark.png">{fonts}<link rel="stylesheet" href="/assets/v2/site.css?v=2.5"><script defer src="/assets/v2/site.js?v=2.4"></script><script type="application/ld+json">{json.dumps(sd,ensure_ascii=False).replace('<','\\u003c')}</script></head>'''
def nav(l,suffix=''):
 urls=[home(l)+'#about',home(l)+'#portfolio',home(l)+'#philosophy',f'/{l}/ir/',home(l)+'#contact']
 links=''.join(f'<a href="{u}"'+(' class="ir-link"' if i==3 else '')+'>'+e(label)+'</a>' for i,(u,label) in enumerate(zip(urls,c(l,'nav'))))
 langs=''.join(f'<li><a href="/{key}/{suffix if key in PUBLISHED else ""}" lang="{key}"'+(' aria-current="page"' if key==l else '')+'>'+e(value['label'])+('' if key in PUBLISHED else '<small>In preparation</small>')+'</a></li>' for key,value in CFG['locales'].items())
 return f'<a class="skip" href="#main">{c(l,"skip")}</a><header class="site-header"><div class="wrap header-inner">{logo(l)}<nav class="desktop-nav" aria-label="Main">{links}</nav><details class="language"><summary aria-label="{c(l,"language")}">{l.upper()}</summary><ul>{langs}</ul></details><details class="mobile-menu"><summary>{c(l,"menu")}</summary><nav aria-label="Mobile">{links}</nav></details></div></header>'
def footer(l):
 pol=''.join(f'<li>{link(url,name,"")}</li>' for name,url in POLICIES)
 ko=l=='ko'
 col=lambda t,items:'<div><b>'+e(t)+'</b>'+''.join(link(u,n,'') for n,u in items)+'</div>'
 cols=col('AP Holdings' ,[(('회사 소개' if ko else 'About'),f'/{l}/about/'),('IR / INVESTORS',f'/{l}/ir/'),('Founder’s Lab',f'/{l}/lab/')])
 cols+=col('Decision Intelligence',[(prod(l,x)['name'],ph(l,x)) for x in ['safe','light','revenue','travel']])
 cols+=col('Commerce',[(prod(l,x)['name'],ph(l,x)) for x in ['select','commerce','craft','lia']])
 cols+=col('Play & Learn',[(prod(l,x)['name'],ph(l,x)) for x in ['rgrg','cubs','lastwave']])
 cols+=col(('커넥터' if ko else 'Connectors'),[(('세이프리스트 · 클로드' if ko else 'Safelist · Claude'),'/business/safelist-connect.html'),(('라이트리스트 · 클로드' if ko else 'Lightlist · Claude'),'/business/lightlist-connect.html')])
 contact_line=f'<div class="footer-contact"><div><span class="eyebrow">CONTACT</span><h3>Build with AP.</h3><p>{c(l,"contact")}</p></div><div>{link("mailto:"+CFG["contact"],CFG["contact"],"contact-email")}{button(mail("Partnership enquiry"),c(l,"contactCta"),True)}</div></div>'
 return f'<footer class="site-footer"><div class="wrap">{contact_line}<div class="footer-top">{logo(l)}<div class="footer-map">{cols}</div></div><ul class="footer-policies" aria-label="{c(l,"privacy")}">{pol}</ul><div class="footer-bottom"><span>© 2026 AP Holdings. All rights reserved.</span><span>Built in Korea. Designed for the world.</span>{link('#top',c(l,'top'),'')}</div></div></footer>'
def shell(l,title,desc,path,body,suffix='',index=True):return head(l,title,desc,path,index,suffix)+'<body id="top">'+nav(l,suffix)+'<main id="main">'+body+'</main>'+footer(l)+'</body></html>\n'
def intro(label,title,desc=''):return f'<div class="section-intro"><div><span class="eyebrow">{e(label)}</span><h2>{e(title)}</h2></div>'+('<p>'+e(desc)+'</p>' if desc else '')+'</div>'
def contact(l):return f'<section class="contact-section anchor" id="contact"><div class="wrap"><span class="eyebrow">CONTACT</span><h2>{c(l,"contactTitle")}</h2><p>{c(l,"contact")}</p><div class="contact-bottom"><div>{link("mailto:"+CFG["contact"],CFG["contact"],"contact-email")}<p class="note">{c(l,"emailNote")}</p></div>{button(mail("Partnership enquiry"),c(l,"contactCta"),True)}</div></div></section>'
def portnav(l):return '<div class="wrap"><div class="three portfolio-nav">'+''.join(f'<a href="{home(l)}#{gid}"><span class="number">0{i+1}</span><h2>{title}</h2><p>{tag}</p></a>' for i,(gid,title,tag,_) in enumerate(GROUPS))+'</div></div>'
def card(l,p,image=False):
 im=f'<img src="{p["image"]}" alt="{e(p["name"])} — {e(c(l,"history"))}" loading="lazy" width="600" height="340">' if image and p.get('image') else ''
 return f'<article class="product-card {"image-card "+p["id"] if im else ""}">{im}'+('<div class="card-body">' if im else '')+status(l,p['status'])+f'<h3>{e(p["name"])}</h3><p class="tag">{e(p["tag"])}</p><p class="desc">{e(p["desc"])}</p>'+ (f'<p class="note">{e(p["note"])}</p>' if p['id'] in ['safe','revenue','craft'] else '')+link(ph(l,p['id']),c(l,'learnMore'))+('</div>' if im else '')+'</article>'
def expert(l):return f'<div class="expert"><span class="eyebrow">EXTERNAL KNOWLEDGE LAYER</span><h3>{c(l,"expertTitle")}</h3><p>{c(l,"expert")}</p>{tags(c(l,"expertPrinciples"))}<p class="note" style="margin-top:24px">{c(l,"expertBoundary")}</p></div>'
def select(l):
 p=prod(l,'select')
 tagline='<p style="margin-top:12px">See it. Try it. Understand it. Choose it.</p>' if l=='ko' else ''
 return f'<article class="select-feature">{status(l,p["status"])}<h3>AP SELECT</h3><h4>A store designed<br>for choosing.</h4><p class="select-kr">{c(l,"selectKo")}</p>{tagline}<p class="desc">{e(p["desc"])}</p><div class="channels"><div><b>OFFLINE</b><span>Experience + Decision</span></div><div><b>ONLINE</b><span>Transaction + Fulfillment</span></div></div>{flow(p["flow"])}<div class="actions">{button(ph(l,"select"),c(l,"learnMore"))}</div></article>'
def lia(l):
 p=prod(l,'lia');return f'<article class="lia-feature"><div class="photo"><img src="{p["image"]}" width="800" height="800" loading="lazy" alt="LIA — AI-generated Korea discovery character"></div><div class="content">{status(l,p["status"])}<h3>Meet LIA.</h3><h4>Discover Korea.</h4><p>{e(p["desc"])}</p><p class="note">{e(p["note"])}</p><div class="actions">{link(ph(l,"lia"),c(l,"learnMore"))}{link("https://www.instagram.com/lia_park55/","Instagram","text-link",True)}{link("https://www.tiktok.com/@lia_park55","TikTok","text-link",True)}</div></div></article>'
def global_section(l):
 blocks=''.join(f'<article><h3>{t}</h3><p>{e(c(l,"core")[i])}</p></article>' for i,t in enumerate(['GLOBAL CORE','MARKET CONFIGURATION','LOCAL ADAPTERS']))
 return f'<section id="global" class="section dark"><div class="wrap"><span class="eyebrow">COMPANY PRINCIPLE / GLOBAL-BY-DESIGN</span><h2>Built in Korea.<br>Designed for the world.</h2><p style="margin-top:28px;font-size:22px">Every AP product is Global-by-Design.</p><p class="muted" style="margin-top:20px;max-width:820px">{c(l,"global")}</p><div class="global-blocks">{blocks}</div><div class="market-detail"><h3>{c(l,"marketTitle")}</h3><p>{c(l,"market")}</p>{tags(MARKET)}<p class="note" style="margin-top:25px">{c(l,"marketReview")}</p><p class="note" style="margin-top:15px">{c(l,"globalNote")}</p></div></div></section>'
def about(l):
 caps='<ul class="founder-list">'+''.join('<li>'+x+'</li>' for x in CAPABILITIES)+'</ul>'
 return f'<section id="about" class="section"><div class="wrap"><span class="eyebrow">ABOUT AP HOLDINGS</span><div class="split"><div><h2>{c(l,"founderTitle")}</h2><p style="margin-top:28px">{c(l,"origin")}</p><p class="note">Mission — {c(l,"mission")}<br>Vision — {c(l,"vision")}</p></div><div><h3>Founder Capability</h3><p style="margin-top:24px">{c(l,"founder")}</p>{caps}<p class="note">{c(l,"firewall")}</p>{link(f"/{l}/ir/",'IR / INVESTORS')}</div></div></div></section>'
def lab(l,full=False):
 cards=''.join(f'<article class="lab-card"><h3>{e(n)}</h3><p>{e(d)}</p>{link("https://apps.apple.com/kr/app/id"+app,"App Store ↗","text-link",True)}</article>' for n,d,app,_ in DATA[l]['lab'][:None if full else 3])
 head=f'<div class="lab-head"><div><span class="eyebrow">FOUNDER’S LAB</span><h2>{"창업자의 독립 프로젝트." if l=="ko" else "Founder’s Lab"}</h2><p>{"핵심 사업 밖에서 만들고 배운 것들." if l=="ko" else "Ideas we build, test and learn from."}</p></div></div>' if not full else f'<div class="lab-head"><div><span class="eyebrow">INDEPENDENT PROJECTS / EXPERIMENTS</span><h2>Founder’s Lab</h2><p>Ideas we build, test and learn from.</p><p style="margin-top:13px">{c(l,"labDesc")}</p></div><p class="note">Build → Release → Learn.</p></div>'
 return f'<section class="lab" id="lab"><div class="wrap">{head}<div class="lab-cards">{cards}</div><div class="actions">{link(f"/{l}/lab/",c(l,"labMore")) if not full else ''}</div></div></section>'
def home_page(l):
 h=HOME_COPY[l];detail=h['detail'];play='영상 재생' if l=='ko' else 'Play film';pause='영상 정지' if l=='ko' else 'Pause film'
 hero=f'<section class="hero home-hero"><div class="wrap"><span class="eyebrow">AP HOLDINGS</span><h1><span class="hero-line">We turn complexity</span> <span class="hero-line">into <em>systems.</em></span></h1><p class="brand-line">Data. Expertise. Process. Technology.</p><p class="lead">{e(h["hero"])}</p></div></section>'
 engine_steps='<ol class="engine-steps">'+''.join(f'<li><span>0{i+1}</span><h3>{e(title)}</h3><p>{e(desc)}</p></li>' for i,(title,desc) in enumerate(h['engineSteps']))+'</ol>'
 featured=f'<section class="home-engine home-featured" id="featured"><div class="wrap"><span class="eyebrow">HOW IT WORKS</span><h2>{e(h["featured"])}</h2><p class="engine-intro">{e(h["engineIntro"])}</p>{engine_steps}<p class="note">{e(h["engineNote"])}</p></div></section>'
 select_visual=f'<div class="film-stage select-visual"><div class="film-picture"><img src="{SELECT_MEDIA["poster"]}" alt="AP SELECT — product comparison and QR order concept" width="1600" height="900" loading="lazy"><video id="select-motion" muted loop playsinline preload="none" poster="{SELECT_MEDIA["poster"]}" data-src="{SELECT_MEDIA["video"]}" aria-hidden="true"></video></div><div class="film-controls"><span>{e(h["concept"])}</span><button class="film-toggle" type="button" aria-controls="select-motion" aria-pressed="false" data-play="{play}" data-pause="{pause}" hidden>{play}</button></div></div>'
 select_text=f'<div class="showcase-copy"><span class="eyebrow">AP SELECT</span><h3>A store designed<br>for choosing.</h3><p>{e(h["select"])}</p>'+('<p class="select-steps">See it. Try it. Understand it. Choose it.</p>' if l=='ko' else '')+f'<div class="actions">{button(ph(l,"select"),detail)}{link(ph(l,"select"),"Expert Collaboration", "quiet-link")}</div></div>'
 select_feature=f'<article class="showcase-select">{select_visual}{select_text}</article>'
 lia_feature=f'<article class="showcase-lia"><a class="showcase-lia-image" href="{ph(l,"lia")}"><img src="/media/lia/lia_hero_sq.jpg" width="800" height="800" loading="lazy" alt="LIA — AI Influencer"></a><div class="showcase-copy"><span class="eyebrow">LIA / AI INFLUENCER</span><h3>Meet LIA.<br>Discover Korea.</h3><p>{e(h["lia"])}</p><p class="lia-channel">{e(h["liaChannel"])}</p>{link(ph(l,"lia"),detail)}</div></article>'
 images={'safe':'/media/safelist_frame.jpg','travel':'/media/inbound_frame.jpg','commerce':'/media/shop/01_dalba.jpg','craft':'/media/craft_frame.jpg','cubs':'/media/cubs/screens.jpg','lastwave':'/media/games/lw_pov_lotte.jpg'}
 def compact(pid):
  p=prod(l,pid)
  return f'<a class="compact-project" href="{ph(l,pid)}"><div class="compact-image {pid}"><img src="{images[pid]}" alt="{e(p["name"])}" loading="lazy" width="480" height="300"></div><div class="compact-copy"><h4>{e(p["name"])}</h4><p>{e(h["short"][pid])}</p><span class="compact-arrow" aria-hidden="true">↗</span></div></a>'
 decision_cards=''
 for pid in ['safe','light','revenue','travel']:
  p=prod(l,pid);example=h['examples'][pid]
  visual=f'<img src="{images[pid]}" alt="{e(p["name"])} — product concept" width="800" height="450" loading="lazy">' if pid in images else '<div class="revenue-example"><span>AP LIGHT</span><strong>'+('한 봉지 465kcal' if l=='ko' else 'One bag: 465 kcal')+'</strong><div>'+('포장 뒷면은 100g당 517kcal' if l=='ko' else 'Back label says 517 kcal / 100 g')+'</div></div>' if pid=='light' else '<div class="revenue-example"><span>'+('GOOD MORNING · 10월 10일' if l=='ko' else 'GOOD MORNING · Oct 10')+'</span><strong>'+('이 날짜가 위험합니다.' if l=='ko' else 'This date is at risk.')+'</strong><div>'+('점유율 45% · 같은 시점 예약 −44% · 취소 35%' if l=='ko' else 'OCC 45% · Same-lead bookings −44% · Cancellations 35%')+'</div></div>'
  pl=h.get('proofLabels',{}).get(pid)
  note=(f'<p class="visual-caption">{e(h["safeNote"])}</p>' if pid=='safe' else '')+(f'<p class="proof-label">{e(pl)}</p>' if pl else f'<p class="proof-label">{e(h["proof"])}</p>' if pid=='revenue' else '')
  decision_cards+=f'<article class="engine-product"><a class="engine-product-visual" href="{ph(l,pid)}">{visual}</a><div class="engine-product-copy"><span class="eyebrow">{e(example[0])}</span><h4>{e(p["name"])}</h4><p>{e(h["short"][pid])}</p><dl><div><dt>{e(h["input"])}</dt><dd>{e(example[1])}</dd></div><div><dt>{e(h["output"])}</dt><dd>{e(example[2])}</dd></div></dl>{note}<div class="actions">{link(p["link"],p["linkLabel"],"button",True) if pid=="revenue" and p.get("link") else ""}{link(ph(l,pid),detail)}</div></div></article>'
 d=h.get('decision')
 if d:
  sv=prod(l,'safe')
  safe_visual=f'<div class="film-stage select-visual"><div class="film-picture"><img src="{sv["image"]}" alt="AP Safe — scanning a snack bag" width="1600" height="900" loading="lazy"><video id="safe-motion" muted loop playsinline preload="none" poster="{sv["image"]}" data-src="{sv["video"]}" aria-hidden="true"></video></div><div class="film-controls"><span>{e(h["concept"])}</span><button class="film-toggle" type="button" aria-controls="safe-motion" aria-pressed="false" data-play="{play}" data-pause="{pause}" hidden>{play}</button></div></div>'
  safe_text=f'<div class="showcase-copy"><span class="eyebrow">AP SAFE</span><h3>{e(d["safeTitle"][0])}<br>{e(d["safeTitle"][1])}</h3><p>{e(d["safe"])}</p><p class="select-steps">{e(d["safeSub"])}</p><div class="actions">{button(ph(l,"safe"),detail)}{link("/business/safelist-connect.html",d["safeQuiet"],"quiet-link")}</div></div>'
  light_feature=f'<article class="showcase-lia"><a class="showcase-lia-image" href="{ph(l,"light")}"><img src="/media/decision/light_card.jpg" width="1200" height="675" loading="lazy" alt="AP Light — 한 봉지 465kcal"></a><div class="showcase-copy"><span class="eyebrow">AP LIGHT / 라이트리스트</span><h3>{e(d["lightTitle"][0])}<br>{e(d["lightTitle"][1])}</h3><p>{e(d["light"])}</p><p class="lia-channel">{e(d["lightSub"])}</p>{link(ph(l,"light"),detail)}</div></article>'
  def compact2(pid,img,alt,desc):
   p=prod(l,pid)
   return f'<a class="compact-project" href="{ph(l,pid)}"><div class="compact-image {pid}"><img src="{img}" alt="{e(alt)}" loading="lazy" width="480" height="300"></div><div class="compact-copy"><h4>{e(p["name"])}</h4><p>{e(desc)}</p><span class="compact-arrow" aria-hidden="true">↗</span></div></a>'
  decision_showcase=f'<article class="showcase-select">{safe_visual}{safe_text}</article><div class="commerce-extras">{light_feature}<div class="compact-grid">'+compact2('revenue','/media/gfx/revenue_goodmorning.jpg','AP Revenue — 예약 페이스 그래프, 작년 대비',d['revenue'])+compact2('travel','/media/inbound_frame.jpg','AP Travel',d['travel'])+'</div></div>'
 else:
  decision_showcase='<div class="engine-product-grid">'+decision_cards+'</div>'
 rgrg=f'<article class="rgrg-feature"><div class="rgrg-stage"><span class="rgrg-star" aria-hidden="true">✦</span><div class="rgrg-title">RGRG <span>오~알지</span></div><img src="/media/games/qa_shot_01.jpg" width="1396" height="644" alt="RGRG — existing quiz battle game interface" loading="lazy"></div><div class="rgrg-copy"><span class="eyebrow">GLOBAL LEARNING GAME</span><h4>{e(h["rgrgTag"])}</h4><p>{e(h["rgrgPacks"])}</p><p class="visual-caption">{e(h["rgrgNote"])}</p>{link(ph(l,"rgrg"),detail)}</div></article>'
 groups=''
 for i,(gid,title,tag,ids) in enumerate(GROUPS):
  contents=decision_showcase if gid=='decision' else select_feature+'<div class="commerce-extras">'+lia_feature+'<div class="compact-grid">'+compact('commerce')+compact('craft')+'</div></div>' if gid=='commerce' else rgrg+'<div class="compact-grid games-grid">'+compact('cubs')+compact('lastwave')+'</div>'
  groups+=f'<section class="portfolio-group" id="{gid}" aria-label="{e(title)}"><div class="group-head"><span>0{i+1}</span><h3>{e(h["groups"][i])}</h3></div><p class="group-desc">{e(h["groupDesc"][i])}</p>{contents}</section>'
 portfolios=f'<section class="home-portfolio section soft" id="portfolio"><div class="wrap"><div class="section-head"><span class="eyebrow">OUR BUSINESSES</span><h2>{e(h["portfolio"])}</h2></div>{groups}</div></section>'
 why=f'<section class="home-why section" id="philosophy"><div class="wrap"><span class="eyebrow">WHY AP</span><h2>{e(h["why"])}</h2><div class="principles">'+''.join(f'<article><h3>{n}</h3><p>{e(h["principles"][i])}</p></article>' for i,n in enumerate(['DATA','EXPERTISE','PROCESS','TECHNOLOGY']))+'</div></div></section>'
 global_short=f'<section class="home-global section dark" id="global"><div class="wrap"><span class="eyebrow">Global-by-Design</span><h2>Built in Korea.<br>Designed for the world.</h2><p class="global-core-line">One core. Multiple markets.</p><p class="global-keywords">Language · Currency · Policy · Partner</p><div class="actions">{link(f"/{l}/ir/#global",h["globalMore"])}</div></div></section>'
 about_short=f'<section class="home-about section" id="about"><div class="wrap"><div class="split"><div><span class="eyebrow">ABOUT AP HOLDINGS</span><h2>{e(h["aboutTitle"])}</h2></div><div><p>{e(h["about"])}</p><div class="actions">{button(f"/{l}/about/",h["aboutMore"])}{button(f"/{l}/ir/","IR / INVESTORS",True)}</div></div></div></div></section>'+lab(l)
 contact_short=f'<section class="contact-section home-contact" id="contact"><div class="wrap"><span class="eyebrow">CONTACT</span><div class="contact-bottom"><div><h2>Build with AP.</h2><p>{e(h["contact"])}</p></div>{button(mail("Partnership enquiry"),c(l,"contactCta"),True)}</div></div></section>'
 intro_items=h.get('portfolioIntro') or [tag for _,_,tag,_ in GROUPS]
 three=f'<section class="section" id="businesses" style="padding-top:28px;padding-bottom:64px"><div class="wrap" style="text-align:center"><span class="eyebrow">THREE BUSINESSES · ONE SYSTEM</span><div class="product-media" style="background:transparent;padding:0;margin:0 auto;max-width:1100px"><img src="/media/gfx/three_businesses.jpg" alt="Decision Intelligence · Commerce · Play &amp; Learn — one AP engine" width="1600" height="820" loading="eager"></div></div></section>'
 return hero+three+portfolios+why+global_short+about_short+contact_short
def ir_page(l):
 hero=f'<section class="page-hero"><div class="wrap"><span class="eyebrow">IR / INVESTORS · PUBLIC IR v2.0</span><h1>{c(l,"irTitle")}</h1><p class="lead">{c(l,"irIntro")}</p><div class="actions">{button("#materials",c(l,"request"),True)}{link(home(l)+"#portfolio",c(l,"explore"))}</div></div></section>'
 navitems=[('thesis','Investment Thesis'),('capability','Founder Capability'),('model','AP Operating Model'),('proof','Working Proof'),('global','Global-by-Design'),('portfolios','Portfolio'),('evidence','Execution Evidence'),('milestones','Milestones'),('roadmap','Global Roadmap'),('materials','Investor Contact')]
 sub='<div class="wrap"><nav class="ir-nav" aria-label="Investor sections">'+''.join(link('#'+i,t,'') for i,t in navitems)+'</nav>'
 def section(id,label,title,body):return f'<section class="ir-section" id="{id}"><span class="eyebrow">{label}</span><h2>{title}</h2>{body}</section>'
 thesis=section('thesis','01 / INVESTMENT THESIS','We turn complexity into systems.',f'<p class="body">{c(l,"investThesis")}</p><p class="quote">{c(l,"origin")}</p>')
 founder=section('capability','02 / FOUNDER CAPABILITY',c(l,'founderTitle'),f'<p class="body">{c(l,"founder")}</p>{tags(CAPABILITIES)}<p class="note" style="margin-top:25px">{c(l,"firewall")}</p>')
 model=section('model','03 / AP OPERATING MODEL',c(l,'howTitle'),flow(FLOWS)+f'<p class="body">{c(l,"assets")}</p>{tags(ASSETS)}')
 proof=section('proof','04 / WORKING PROOF','AP Revenue',status(l,'working')+f'<p class="body" style="margin-top:24px">{c(l,"proof")}</p><p class="note" style="margin-top:20px">{c(l,"proofNote")}</p><div class="proof"><h3>{c(l,"demoTitle")}</h3><div class="proof-steps">'+''.join(f'<article><b>{t}</b><p>{c(l,"demoSteps")[i]}</p></article>' for i,t in enumerate(['PRIORITY','HUMAN ACTION','OUTCOME']))+f'</div><p class="note">{c(l,"demoNote")}</p></div>')
 # No numeric or operational dashboard is presented. Only a public conceptual workflow.
 portfolios=section('portfolios','06 / PORTFOLIO',c(l,'portIntro'),'<div class="grid-3">'+''.join(f'<article class="evidence-card"><h3>{title}</h3><p>{tag}</p><p>{" · ".join(prod(l,p)["name"] for p in ids)}</p><div class="actions">{link(home(l)+"#"+gid,c(l,"learnMore"))}</div></article>' for gid,title,tag,ids in GROUPS)+'</div>')
 evidence=section('evidence','07 / EXECUTION EVIDENCE',c(l,'futureTitle'),f'<div class="grid-2"><article class="evidence-card"><span class="status">FOUNDER-PROVIDED</span><h3>{c(l,"evidence")}</h3><p>{c(l,"evidenceNote")}</p><div class="actions">{link(ph(l,"cubs"),'Hangeul Cubs')}{link(f"/{l}/lab/",'Founder’s Lab')}</div></article><article class="evidence-card"><span class="status">EARLY EXPERIMENT</span><h3>LIA</h3><p>{c(l,"liaEvidence")}</p><div class="actions">{link(ph(l,"lia"),'Meet LIA')}</div></article></div><p class="body">{c(l,"future")}</p>{tags(["External Pilots","Active Users","Transactions","Revenue","Repeat","Outcome"])}')
 milestones=section('milestones','08 / MILESTONES',c(l,'milestonesTitle'),'<div class="milestones">'+''.join(f'<article><span>{n}</span><h3>{t}</h3><p>{d}</p></article>' for n,t,d in c(l,'milestones'))+f'</div><p class="note" style="margin-top:30px">{c(l,"milestoneNote")}</p>')
 roadmap=section('roadmap','09 / GLOBAL ROADMAP',c(l,'roadmapTitle'),f'<p class="body">{c(l,"roadmap")}</p><p class="note" style="margin-top:25px">{c(l,"globalNote")}</p>')
 materials=section('materials','10 / INVESTOR CONTACT',c(l,'materialsTitle'),'<div class="materials">'+''.join(f'<article><h3>{c(l,k+"Title")}</h3><p>{c(l,k+"Desc")}</p></article>' for k in ['public','share','nda'])+f'</div><div class="actions">{button(mail("Request Investor Materials — IR v2.0"),c(l,"request"),True)}</div><p class="note" style="margin-top:20px">{c(l,"requestNote")}</p><p class="note" style="margin-top:28px">{c(l,"version")}</p>')
 return hero+sub+thesis+founder+model+proof+'</div>'+global_section(l)+'<div class="wrap">'+portfolios+evidence+milestones+roadmap+materials+'</div>'
# Optional evidence sections per product/connector, data-driven from locale JSON. Existing v2 classes only.
def blocks(items):
 h=''
 for b in items:
  t=b.get('type')
  if t=='milestones':h+='<div class="milestones">'+''.join(f'<article><span>{e(a)}</span><h3>{e(bb)}</h3><p>{e(cc)}</p></article>' for a,bb,cc in b['items'])+'</div>'
  elif t=='proof':h+='<div class="proof">'+(f'<h3>{e(b["h3"])}</h3>' if b.get('h3') else '')+(f'<p class="quote">{e(b["quote"])}</p>' if b.get('quote') else '')+(flow(b['flow']).replace('<ol','<ul').replace('</ol>','</ul>') if b.get('flow') else '')+('<ol>'+''.join('<li>'+e(x)+'</li>' for x in b['ol'])+'</ol>' if b.get('ol') else '')+('<div class="proof-steps">'+''.join(f'<div><b>{e(a)}</b><p>{e(bb)}</p></div>' for a,bb in b['steps'])+'</div>' if b.get('steps') else '')+(f'<p>{e(b["p"])}</p>' if b.get('p') else '')+(f'<p class="note">{e(b["note"])}</p>' if b.get('note') else '')+'</div>'
  elif t=='grid2':h+='<div class="grid-2">'+blocks(b['items'])+'</div>'
  elif t=='tags':h+=tags(b['items'])
  elif t=='flow':h+=flow(b['items']).replace('<ol','<ul').replace('</ol>','</ul>')
  elif t=='quote':h+=f'<p class="quote">{e(b["text"])}</p>'
  elif t=='note':h+=f'<p class="note">{e(b["text"])}</p>'
  elif t=='p':h+=f'<p>{e(b["text"])}</p>'
  elif t=='media':h+=f'<figure style="margin:0 0 45px"><div class="product-media" style="background:transparent;padding:0"><img src="{b["src"]}" alt="{e(b["alt"])}" width="1600" height="900" loading="lazy" style="width:100%;max-height:none;border-radius:24px"></div>'+(f'<figcaption class="note">{e(b["caption"])}</figcaption>' if b.get('caption') else '')+'</figure>'
  elif t=='split':h+='<div class="split"><div>'+blocks(b['left'])+'</div><div>'+blocks(b['right'])+'</div></div>'
  elif t=='h3':h+=f'<h3>{e(b["text"])}</h3>'
  elif t=='actions':h+='<div class="actions">'+''.join(button(u,lab,True) if kind=='primary' else button(u,lab) if kind=='button' else link(u,lab) for u,lab,kind in b['items'])+'</div>'
 return h
def sections(items):
 h=''
 for sec in items:
  head_=f'<div class="section-intro"><div><span class="number">{e(sec["label"])}</span><h2>{e(sec["title"])}</h2></div><p>{e(sec["desc"])}</p></div>' if sec.get('desc') else f'<div class="section-head"><span class="number">{e(sec["label"])}</span><h2>{e(sec["title"])}</h2></div>'
  h+=f'<section class="section{" soft" if sec.get("soft") else ""} anchor" id="{e(sec["id"])}"><div class="wrap">{head_}{blocks(sec["blocks"])}</div></section>'
 return h
def product_page(l,p):
 pid=p['id'];body=f'<section class="page-hero"><div class="wrap"><div class="breadcrumb">{link(home(l)+"#portfolio",c(l,"nav")[1],"")} / {e(p["name"])}</div>{status(l,p["status"])}<h1 class="product-name">{e(p["name"])+( " (오~알지)" if pid=="rgrg" and l=="ko" else "")}</h1><h2>{e(p["tag"])}</h2><p class="lead">{e(p["desc"])}</p></div></section><section class="section"><div class="wrap">'
 if pid=='rgrg':
  body+='<figure class="rgrg-detail"><img src="/media/games/qa_shot_01.jpg" alt="RGRG — existing quiz battle interface" width="1396" height="644"><figcaption class="note">'+HOME_COPY[l]['rgrgNote']+'</figcaption></figure>'
 if p.get('heroSplit') and p.get('image'):
  body+=f'<article class="showcase-lia"><a class="showcase-lia-image" href="{p["image"]}"><img src="{p["image"]}" width="800" height="800" loading="lazy" alt="{e(p["name"])}"></a><div class="showcase-copy"><span class="eyebrow">{e(p["role"])}</span><h3>{e(p["tag"])}</h3><p>{e(p["desc"])}</p>'+(f'<div class="actions">'+''.join(button(u,l2) for u,l2 in p.get("heroLinks",[]))+'</div>' if p.get('heroLinks') else '')+'</div></article>'
 elif p.get('image') and pid!='rgrg':
  visual=f'<video autoplay muted loop playsinline preload="metadata" poster="{p["image"]}" src="{p["video"]}" aria-label="{e(p["name"])} — existing concept video"></video>' if p.get('video') else f'<img src="{p["image"]}" alt="{e(p["name"])} — {c(l,"history")}" width="1000" height="600" loading="lazy">'
  body+=f'<figure style="margin:0 0 45px"><div class="product-media">{visual}</div><figcaption class="note">{c(l,"rgrgAssetNote" if pid=="rgrg" else "assetNote")}</figcaption></figure>'
 body+=('<div class="product-body" hidden>' if (p.get('hideGeneric') or p.get('heroSplit')) else f'<div class="product-body"><span class="eyebrow">{e(p["role"])}</span><h2>{e(p["tag"])}</h2>{flow(p["flow"])}<p class="note">{e(p["note"])}</p>')
 if p.get('link'):body+=f'<div class="actions">{link(p["link"],p["linkLabel"],"button",True)}</div>'
 if pid=='safe':body+=f'<p>{c(l,"legacySafe")}</p><div class="actions">{button("/business/safelist-connect.html",c(l,"connector"))}</div>'
 if pid=='light':body+=f'<div class="actions">{button("/business/lightlist-connect.html",c(l,"connector"))}</div>'
 if pid=='revenue':body+=f'<p>{c(l,"proof")}</p><p class="note">{c(l,"proofNote")}</p><div class="actions">{button(f"/{l}/ir/#proof",c(l,"proofTitle"))}</div>'
 if pid=='select' and not p.get('hideGeneric'):body+=f'<p>{c(l,"selectKo")}</p><div class="channels" style="border-color:var(--line)"><div><b>OFFLINE</b><span>Experience + Decision</span></div><div><b>ONLINE</b><span>Transaction + Fulfillment</span></div></div>'+expert(l)
 if pid=='rgrg' and not p.get('hideGeneric'):body+=f'<h2 style="margin-top:40px">{c(l,"rgrgTitle")}</h2><p>{c(l,"rgrg")}</p>{tags(["Vietnamese → Korean","Korean → Vietnamese","Japanese → Korean","French → Korean","Korean → English"])}<p class="note">{c(l,"pairs")}</p>'
 if pid=='lia' and not p.get('heroSplit'):body+=f'<p>{c(l,"liaEvidence")}</p><div class="actions">{link("https://www.instagram.com/lia_park55/","Instagram","button",True)}{link("https://www.tiktok.com/@lia_park55","TikTok","button",True)}</div>'
 if pid=='lastwave' and not p.get('hideGeneric'):body+=f'<h2 style="margin-top:40px">{c(l,"creatorTitle")}</h2><p>{c(l,"creator")}</p>'
 if pid=='lia' and not p.get('hideArchive'):
  body+='<h2 style="margin-top:45px">Content archive</h2><div class="grid-3" style="margin-top:24px">'+''.join(f'<figure style="margin:0"><video controls playsinline preload="none" poster="/media/lia/review_ep{i}_{name}_poster.jpg" src="/media/lia/review_ep{i}_{name}.mp4"></video><figcaption class="note">LIA · {label}</figcaption></figure>' for i,name,label in [(1,'suncream','Sun care'),(2,'mask','Mask'),(3,'tint','Lip tint')])+'</div><p class="note">AI-generated content · '+c(l,'assetNote')+'</p>'
 if pid=='lastwave' and not p.get('hideGeneric'):
  body+='<h2 style="margin-top:45px">Characters &amp; worlds</h2><div class="grid-3" style="margin-top:24px">'+''.join(f'<figure style="margin:0"><img loading="lazy" src="/media/games/{src}" alt="{label}" width="500" height="500"><figcaption class="note">{label}</figcaption></figure>' for src,label in [('lw_hero_pixel.png','PIXEL'),('lw_hero_alfred.png','ALFRED'),('lw_hero_line.png','LINE'),('lw_hero_bluenewbie.png','BLUE NEWBIE'),('lw_hero_rookie.png','ROOKIE'),('lw_pov_gwanghwamun.jpg','World concept')])+'</div>'
 if pid=='commerce':
  body+='<h2 style="margin-top:45px">Curation archive</h2><p class="note">'+c(l,'curationNote')+'</p><div class="grid-3">'+''.join(f'<figure style="margin:0"><img src="/media/shop/{src}.jpg" alt="{label}" loading="lazy" width="400" height="400"><figcaption class="note">{label}</figcaption></figure>' for src,label in [('01_dalba',"d’Alba"),('02_cosrx','COSRX'),('03_tirtir','TIRTIR'),('04_biodance','Biodance'),('06_romnd','rom&nd'),('07_anua','Anua'),('08_skin1004','SKIN1004'),('09_mediheal','Mediheal'),('10_banilaco','banila co')])+'</div>'
 body+='</div></div></section>'+sections(p.get('sections',[]))
 return body
# Generate real, crawlable KO/EN documents; the builder, not client JS, selects copy.
for l in PUBLISHED:
 out(f'{l}/index.html',shell(l,'AP HOLDINGS — We turn complexity into systems.',c(l,'hero'),home(l),home_page(l)))
 out(f'{l}/ir/index.html',shell(l,'IR / INVESTORS — AP Holdings',c(l,'irIntro'),f'/{l}/ir/',ir_page(l),'ir/'))
 out(f'{l}/about/index.html',shell(l,'About — AP Holdings',c(l,'origin'),f'/{l}/about/',about(l).replace('<h2>','<h1>',1).replace('</h2>','</h1>',1),'about/'))
 out(f'{l}/lab/index.html',shell(l,'Founder’s Lab — AP Holdings',c(l,'labDesc'),f'/{l}/lab/',f'<section class="page-hero"><div class="wrap"><span class="eyebrow">INDEPENDENT PROJECTS / EXPERIMENTS</span><h1>Ideas we build,<br>test and learn from.</h1><p class="lead">{c(l,"labDesc")}</p></div></section>'+lab(l,True),'lab/'))
 for p in DATA[l]['products']:
  out(f'{l}/products/{p["id"]}/index.html',shell(l,p['name']+' — AP Holdings',p['desc'],ph(l,p['id']),product_page(l,p),f'products/{p["id"]}/'))
# Keep root as a useful Korean page instead of browser/IP-dependent redirects.
out('index.html',shell('ko','AP HOLDINGS — We turn complexity into systems.',c('ko','hero'),'/ko/',home_page('ko')))
def redirect(path,target):
 out(path,f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AP Holdings</title><meta name="robots" content="noindex,follow"><link rel="canonical" href="{ORIGIN+target}"><meta http-equiv="refresh" content="0;url={target}"></head><body><p><a href="{target}">AP Holdings — 계속 / Continue</a></p></body></html>\n''')
ALIASES={'about.html':'/ko/about/','apps.html':'/ko/lab/','lia.html':'/ko/products/lia/','shop.html':'/ko/products/commerce/','board/index.html':'/ko/','business/safelist.html':'/ko/products/safe/','business/inbound.html':'/ko/products/travel/','business/craft.html':'/ko/products/craft/','business/games.html':'/ko/#games','lastwave/index.html':'/ko/products/lastwave/','ir/index.html':'/ko/ir/','investors/index.html':'/en/ir/','business/lightlist-connect_옛버전_20260921.html':'/ko/products/light/'}
for p in (ROOT/'_backup_20260919').glob('*.html'):ALIASES[str(p.relative_to(ROOT))]='/ko/'
for path,target in ALIASES.items():redirect(path,target)
# Existing remote connector paths stay functional with honest public copy and clipboard fallback.
for pid,old in [('safe','safelist'),('light','lightlist')]:
 p=prod('ko',pid);url=f'https://{old}-mcp.onrender.com/mcp';path=f'/business/{old}-connect.html'
 box=f'<div class="connector-box"><p>{c("ko","connectorNote")}</p><code id="connector-url">{url}</code><button type="button" data-copy-target="connector-url" data-success="{c("ko","copied")}" data-fallback="{c("ko","copyFail")}">{c("ko","copy")}</button><p role="status" class="copy-feedback" aria-live="polite"></p></div>'
 cn=p.get('connector')
 if cn:
  # Evidence-first connector page: hero → (media) → data-driven sections; the box sits where the JSON says.
  hero=f'<section class="page-hero"><div class="wrap"><p class="breadcrumb">{link(home("ko")+"#portfolio",c("ko","nav")[1],"")} / {link(ph("ko",pid),p["name"],"")} / 커넥터</p><span class="status">{e(cn["status"])}</span><span class="eyebrow">{e(cn["eyebrow"])}</span><h1>'+'<br>'.join(e(x) for x in cn['title'])+'</h1><p class="lead">'+'<br>'.join(e(x) for x in cn['lead'])+'</p>'+(box if cn.get('boxInHero') else f'<div class="actions">{button("#connect",cn["cta"],True)}{link(ph("ko",pid),c("ko","learnMore"))}</div>')+'</div></section>'
  media=f'<section class="section"><div class="wrap"><div class="product-media"><video src="{p["video"]}" poster="{p["image"]}" autoplay muted loop playsinline aria-label="{e(cn["mediaAlt"])}"></video></div><p class="note visual-caption">{e(cn["mediaNote"])}</p></div></section>' if cn.get('media') and p.get('video') else ''
  connect='' if cn.get('boxInHero') else f'<section class="section anchor" id="connect"><div class="wrap"><div class="product-body"><span class="number">{e(cn["connectLabel"])}</span><h2>{e(cn["connectTitle"])}</h2><p>{c("ko","connectHelp")}</p>{box}{tags(cn["tools"])}<p class="note">{e(cn["connectNote"])}</p></div></div></section>'
  content=hero+media+sections(cn['sections'])+connect
  desc=' '.join(cn['lead'])
  out(path.lstrip('/'),shell('ko',cn['pageTitle'],desc,path,content,index=False))
  continue
 content=f'<section class="page-hero"><div class="wrap"><span class="eyebrow">{e(p["name"])} / CONNECTOR</span><h1>{e(p["name"])}</h1><p class="lead">{e(p["desc"])}</p></div></section><section class="section"><div class="wrap"><div class="product-body"><h2>{c("ko","connector")}</h2><p>{c("ko","connectHelp")}</p><p class="note">{e(p["note"])}</p>{box}<div class="actions">{button(ph("ko",pid),c("ko","learnMore"))}</div></div></div></section>'
 out(path.lstrip('/'),shell('ko',p['name']+' Connector — AP Holdings',p['desc'],path,content,index=False))
# New localized public pages require human/professional QA. No placeholder translations are indexed.
for l,cfg in CFG['locales'].items():
 if l in PUBLISHED:continue
 content=f'<section class="page-hero"><div class="wrap empty-page"><span class="eyebrow">AP HOLDINGS / {e(cfg["label"])}</span><h1>We turn complexity into systems.</h1><p lang="{l}">{e(cfg["notice"])}</p><div class="actions">{button("/en/","English",True)}{button("/ko/","한국어")}</div></div></section>'
 text=shell('en','AP Holdings — '+cfg['label'],cfg['notice'],f'/{l}/',content,index=False).replace('<html lang="en">',f'<html lang="{l}">',1)
 out(f'{l}/index.html',text)
# Preserve the policy terms and old App Store policy URL; change only the product's display name.
policy=(ROOT/'quizarena_privacy.html').read_text()
policy=re.sub(r'Quiz\s*Arena|퀴즈\s*아레나', 'RGRG', policy, flags=re.I)
policy=re.sub(r'<link rel="canonical"[^>]*>', '', policy)
policy=policy.replace('<head>','<head><link rel="canonical" href="'+ORIGIN+'/rgrg/privacy.html">',1)
out('quizarena_privacy.html',policy)
out('rgrg/privacy.html',policy)
# Sitemap includes approved content only. No private files or planned domain surfaces are linked.
urls=[f'/{l}/{suffix}' for l in PUBLISHED for suffix in ['','ir/','about/','lab/']+[f'products/{p["id"]}/' for p in DATA[l]['products']]]
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN+u}</loc><lastmod>{CFG["date"]}</lastmod></url>' for u in urls)+'</urlset>\n'
out('sitemap.xml',xml)
out('robots.txt','User-agent: *\nAllow: /\nDisallow: /_backup_20260919/\nDisallow: /site-source/\nDisallow: /scripts/\nDisallow: /board/\nDisallow: /data/\nDisallow: /docs/\nDisallow: /vi/\nDisallow: /ja/\nDisallow: /zh-cn/\nDisallow: /fr/\nSitemap: '+ORIGIN+'/sitemap.xml\n')
out('404.html',shell('en','Page not found — AP Holdings','AP Holdings', '/404.html',f'<section class="page-hero"><div class="wrap empty-page"><span class="eyebrow">404</span><h1>Let’s find your way.</h1><div class="actions">{button("/en/","Home",True)}{button("/ko/","한국어")}{button("/en/ir/","IR / INVESTORS")}</div></div></section>',index=False))
(ROOT/'site-source/generated-files.json').write_text(json.dumps(GENERATED,ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(GENERATED)} static files; published locales: {", ".join(PUBLISHED)}. No JS required for content.')

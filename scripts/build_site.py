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
 return f'''<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(description,quote=True)}"><meta name="robots" content="{'index,follow' if index else 'noindex,follow'}"><link rel="canonical" href="{canonical}">{alternates}<meta property="og:type" content="website"><meta property="og:site_name" content="AP Holdings"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:locale" content="{'ko_KR' if l=='ko' else 'en_US'}"><meta name="theme-color" content="#ffffff"><link rel="icon" href="/img/ap_mark.png">{fonts}<link rel="stylesheet" href="/assets/v2/site.css?v=2.1"><script defer src="/assets/v2/site.js?v=2.1"></script><script type="application/ld+json">{json.dumps(sd,ensure_ascii=False).replace('<','\\u003c')}</script></head>'''
def nav(l,suffix=''):
 urls=[home(l)+'#about',home(l)+'#portfolio',home(l)+'#philosophy',f'/{l}/ir/',home(l)+'#contact']
 links=''.join(f'<a href="{u}"'+(' class="ir-link"' if i==3 else '')+'>'+e(label)+'</a>' for i,(u,label) in enumerate(zip(urls,c(l,'nav'))))
 langs=''.join(f'<li><a href="/{key}/{suffix if key in PUBLISHED else ""}" lang="{key}"'+(' aria-current="page"' if key==l else '')+'>'+e(value['label'])+('' if key in PUBLISHED else '<small>In preparation</small>')+'</a></li>' for key,value in CFG['locales'].items())
 return f'<a class="skip" href="#main">{c(l,"skip")}</a><header class="site-header"><div class="wrap header-inner">{logo(l)}<nav class="desktop-nav" aria-label="Main">{links}</nav><details class="language"><summary aria-label="{c(l,"language")}">{l.upper()}</summary><ul>{langs}</ul></details><details class="mobile-menu"><summary>{c(l,"menu")}</summary><nav aria-label="Mobile">{links}</nav></details></div></header>'
def footer(l):
 pol=''.join(f'<li>{link(url,name,"")}</li>' for name,url in POLICIES)
 return f'<footer class="site-footer"><div class="wrap"><div class="footer-top">{logo(l)}<div class="footer-links">{link(home(l)+"#portfolio",c(l,"nav")[1],"")}{link(f"/{l}/ir/","IR / INVESTORS","")}{link(f"/{l}/lab/","Founder’s Lab","")}{link(home(l)+"#contact",c(l,"nav")[4],"")}</div></div><ul class="footer-policies" aria-label="{c(l,"privacy")}">{pol}</ul><div class="footer-bottom"><span>© 2026 AP Holdings. All rights reserved.</span><span>Built in Korea. Designed for the world.</span>{link('#top',c(l,'top'),'')}</div></div></footer>'
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
 return f'<section class="lab" id="lab"><div class="wrap"><div class="lab-head"><div><span class="eyebrow">INDEPENDENT PROJECTS / EXPERIMENTS</span><h2>Founder’s Lab</h2><p>Ideas we build, test and learn from.</p><p style="margin-top:13px">{c(l,"labDesc")}</p></div><p class="note">Build → Release → Learn.</p></div><div class="lab-cards">{cards}</div><div class="actions">{link(f"/{l}/lab/",c(l,"labMore")) if not full else ''}</div></div></section>'
def home_page(l):
 play='영상 재생' if l=='ko' else 'Play film'
 pause='영상 정지' if l=='ko' else 'Pause film'
 caption='복잡성의 구조화 · AI 브랜드 콘셉트' if l=='ko' else 'Complexity, composed. · AI brand concept'
 hero=f'<section class="hero"><div class="wrap"><span class="eyebrow">AP HOLDINGS</span><h1><span class="hero-line">We turn complexity</span> <span class="hero-line">into <em>systems.</em></span></h1><p class="brand-line">Data. Expertise. Process. Technology.</p><p class="lead">{c(l,"hero")}</p><div class="actions">{button("#portfolio",c(l,"explore"),True)}{link("#about",c(l,"aboutCta"))}</div><figure class="brand-film"><div class="film-stage"><img src="{MEDIA["poster"]}" alt="" width="1600" height="900" fetchpriority="high"><video id="brand-motion" muted loop playsinline preload="none" poster="{MEDIA["poster"]}" data-src="{MEDIA["video"]}" aria-label="{caption}" aria-hidden="true"></video><button class="film-toggle" type="button" aria-controls="brand-motion" aria-pressed="false" data-play="{play}" data-pause="{pause}" hidden>{play}</button></div><figcaption><span>{caption}</span><strong>Built in Korea. Designed for the world.</strong></figcaption></figure></div></section>'

 why=f'<section class="section" id="philosophy"><div class="wrap">{intro("WHY AP",c(l,"whyTitle"),c(l,"why"))}<div class="principles">'+''.join(f'<article><h3>{name}</h3><p>{e(c(l,"how")[i])}</p></article>' for i,name in enumerate(['DATA','EXPERTISE','PROCESS','TECHNOLOGY']))+f'</div><div class="operating-model">{flow(FLOWS)}</div></div></section>'
 portfolios=f'<section class="section soft" id="portfolio"><div class="wrap">{intro("WHAT WE BUILD",c(l,"portIntro"),c(l,"portDesc"))}</div>{portnav(l)}</section>'
 decision=f'<section class="section" id="decision"><div class="wrap"><div class="section-head"><span class="number">01 / DECISION INTELLIGENCE</span><h2>From data to<br>clearer action.</h2><p>{c(l,"decisionDesc")}</p></div><div class="grid-2">'+''.join(card(l,prod(l,p)) for p in GROUPS[0][3])+f'</div><p class="quote">Safe protects the boundary. Light explains the choice. Experts add judgment. People decide. Outcomes create learning.</p></div></section>'
 commerce=f'<section class="section" id="commerce"><div class="wrap"><div class="section-head"><span class="number">02 / COMMERCE</span><h2>From discovery to choice<br>to transaction.</h2></div>{select(l)}<div class="grid-2">{card(l,prod(l,"commerce"))}{card(l,prod(l,"craft"))}</div>{lia(l)}{expert(l)}</div></section>'
 games=f'<section class="section soft" id="games"><div class="wrap"><div class="section-head"><span class="number">03 / GAMES, LEARNING &amp; IP</span><h2>Play. Learn. Create.</h2><p>{c(l,"gameDesc")}</p></div><div class="grid-3">'+''.join(card(l,prod(l,p),True) for p in GROUPS[2][3])+f'</div><div class="expert"><h3>{c(l,"rgrgTitle")}</h3><p>{c(l,"rgrg")}</p>{flow(prod(l,"rgrg")["flow"])}<p class="note">Vietnamese → Korean · Korean → Vietnamese · Japanese → Korean · French → Korean · Korean → English<br>{c(l,"pairs")}</p></div></div></section>'
 assets=f'<section class="section" id="assets"><div class="wrap">{intro("ONE AP PHILOSOPHY",c(l,"assetsTitle"),c(l,"assets"))}{tags(ASSETS)}</div></section>'
 return hero+portfolios+why+global_section(l)+decision+commerce+games+assets+about(l)+lab(l)+contact(l)
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
 return hero+sub+thesis+founder+model+proof+'</div>'+global_section(l)+'<div class="wrap">'+portfolios+evidence+milestones+roadmap+materials+'</div>'+contact(l)
def product_page(l,p):
 pid=p['id'];body=f'<section class="page-hero"><div class="wrap"><div class="breadcrumb">{link(home(l)+"#portfolio",c(l,"nav")[1],"")} / {e(p["name"])}</div>{status(l,p["status"])}<h1 class="product-name">{e(p["name"])+( " (오~알지)" if pid=="rgrg" and l=="ko" else "")}</h1><h2>{e(p["tag"])}</h2><p class="lead">{e(p["desc"])}</p></div></section><section class="section"><div class="wrap">'
 if p.get('image'):body+=f'<figure style="margin:0 0 45px"><div class="product-media"><img src="{p["image"]}" alt="{e(p["name"])} — {c(l,"history")}" width="1000" height="600" loading="lazy"></div><figcaption class="note">{c(l,"rgrgAssetNote" if pid=="rgrg" else "assetNote")}</figcaption></figure>'
 body+=f'<div class="product-body"><span class="eyebrow">{e(p["role"])}</span><h2>{e(p["tag"])}</h2>{flow(p["flow"])}<p class="note">{e(p["note"])}</p>'
 if p.get('link'):body+=f'<div class="actions">{link(p["link"],p["linkLabel"]+" ↗","button",True)}</div>'
 if pid=='safe':body+=f'<p>{c(l,"legacySafe")}</p><div class="actions">{button("/business/safelist-connect.html",c(l,"connector"))}</div>'
 if pid=='light':body+=f'<div class="actions">{button("/business/lightlist-connect.html",c(l,"connector"))}</div>'
 if pid=='revenue':body+=f'<p>{c(l,"proof")}</p><p class="note">{c(l,"proofNote")}</p><div class="actions">{button(f"/{l}/ir/#proof",c(l,"proofTitle"))}</div>'
 if pid=='select':body+=f'<p>{c(l,"selectKo")}</p><div class="channels" style="border-color:var(--line)"><div><b>OFFLINE</b><span>Experience + Decision</span></div><div><b>ONLINE</b><span>Transaction + Fulfillment</span></div></div>'+expert(l)
 if pid=='rgrg':body+=f'<h2 style="margin-top:40px">{c(l,"rgrgTitle")}</h2><p>{c(l,"rgrg")}</p>{tags(["Vietnamese → Korean","Korean → Vietnamese","Japanese → Korean","French → Korean","Korean → English"])}<p class="note">{c(l,"pairs")}</p>'
 if pid=='lia':body+=f'<p>{c(l,"liaEvidence")}</p><div class="actions">{link("https://www.instagram.com/lia_park55/","Instagram ↗","button",True)}{link("https://www.tiktok.com/@lia_park55","TikTok ↗","button",True)}</div>'
 if pid=='lastwave':body+=f'<h2 style="margin-top:40px">{c(l,"creatorTitle")}</h2><p>{c(l,"creator")}</p>'
 if pid=='lia':
  body+='<h2 style="margin-top:45px">Content archive</h2><div class="grid-3" style="margin-top:24px">'+''.join(f'<figure style="margin:0"><video controls playsinline preload="none" poster="/media/lia/review_ep{i}_{name}_poster.jpg" src="/media/lia/review_ep{i}_{name}.mp4"></video><figcaption class="note">LIA · {label}</figcaption></figure>' for i,name,label in [(1,'suncream','Sun care'),(2,'mask','Mask'),(3,'tint','Lip tint')])+'</div><p class="note">AI-generated content · '+c(l,'assetNote')+'</p>'
 if pid=='lastwave':
  body+='<h2 style="margin-top:45px">Characters &amp; worlds</h2><div class="grid-3" style="margin-top:24px">'+''.join(f'<figure style="margin:0"><img loading="lazy" src="/media/games/{src}" alt="{label}" width="500" height="500"><figcaption class="note">{label}</figcaption></figure>' for src,label in [('lw_hero_pixel.png','PIXEL'),('lw_hero_alfred.png','ALFRED'),('lw_hero_line.png','LINE'),('lw_hero_bluenewbie.png','BLUE NEWBIE'),('lw_hero_rookie.png','ROOKIE'),('lw_pov_gwanghwamun.jpg','World concept')])+'</div>'
 if pid=='commerce':
  body+='<h2 style="margin-top:45px">Curation archive</h2><p class="note">'+c(l,'curationNote')+'</p><div class="grid-3">'+''.join(f'<figure style="margin:0"><img src="/media/shop/{src}.jpg" alt="{label}" loading="lazy" width="400" height="400"><figcaption class="note">{label}</figcaption></figure>' for src,label in [('01_dalba',"d’Alba"),('02_cosrx','COSRX'),('03_tirtir','TIRTIR'),('04_biodance','Biodance'),('06_romnd','rom&nd'),('07_anua','Anua'),('08_skin1004','SKIN1004'),('09_mediheal','Mediheal'),('10_banilaco','banila co')])+'</div>'
 body+='</div></div></section>'+contact(l)
 return body
# Generate real, crawlable KO/EN documents; the builder, not client JS, selects copy.
for l in PUBLISHED:
 out(f'{l}/index.html',shell(l,'AP HOLDINGS — We turn complexity into systems.',c(l,'hero'),home(l),home_page(l)))
 out(f'{l}/ir/index.html',shell(l,'IR / INVESTORS — AP Holdings',c(l,'irIntro'),f'/{l}/ir/',ir_page(l),'ir/'))
 out(f'{l}/about/index.html',shell(l,'About — AP Holdings',c(l,'origin'),f'/{l}/about/',about(l).replace('<h2>','<h1>',1).replace('</h2>','</h1>',1)+contact(l),'about/'))
 out(f'{l}/lab/index.html',shell(l,'Founder’s Lab — AP Holdings',c(l,'labDesc'),f'/{l}/lab/',f'<section class="page-hero"><div class="wrap"><span class="eyebrow">INDEPENDENT PROJECTS / EXPERIMENTS</span><h1>Ideas we build,<br>test and learn from.</h1><p class="lead">{c(l,"labDesc")}</p></div></section>'+lab(l,True)+contact(l),'lab/'))
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
 content=f'<section class="page-hero"><div class="wrap"><span class="eyebrow">{e(p["name"])} / CONNECTOR</span><h1>{e(p["name"])}</h1><p class="lead">{e(p["desc"])}</p></div></section><section class="section"><div class="wrap"><div class="product-body"><h2>{c("ko","connector")}</h2><p>{c("ko","connectHelp")}</p><p class="note">{e(p["note"])}</p><div class="connector-box"><p>{c("ko","connectorNote")}</p><code id="connector-url">{url}</code><button type="button" data-copy-target="connector-url" data-success="{c("ko","copied")}" data-fallback="{c("ko","copyFail")}">{c("ko","copy")}</button><p role="status" class="copy-feedback" aria-live="polite"></p></div><div class="actions">{button(ph("ko",pid),c("ko","learnMore"))}</div></div></div></section>'
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

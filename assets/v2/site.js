'use strict';
// Navigation and clipboard enhancement; the complete content is available without JS.
document.querySelectorAll('details').forEach((detail) => {
  detail.addEventListener('toggle', () => {
    if (detail.open) document.querySelectorAll('details[open]').forEach((other) => { if (other !== detail) other.open = false; });
  });
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') document.querySelectorAll('details[open]').forEach((detail) => { detail.open = false; detail.querySelector('summary')?.focus(); });
});
document.addEventListener('click', (event) => {
  document.querySelectorAll('details[open]').forEach((detail) => { if (!detail.contains(event.target)) detail.open = false; });
  if (event.target.closest('.mobile-menu a')) document.querySelector('.mobile-menu').open = false;
});
document.querySelectorAll('[data-copy-target]').forEach((button) => {
  button.addEventListener('click', async () => {
    const code = document.getElementById(button.dataset.copyTarget);
    const feedback = button.parentElement.querySelector('[role="status"]');
    try {
      if (!navigator.clipboard) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(code.textContent.trim());
      feedback.textContent = button.dataset.success;
    } catch {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(code);
      selection.removeAllRanges(); selection.addRange(range);
      feedback.textContent = button.dataset.fallback;
    }
  });
});
// Preserve existing inbound links to the former home section IDs.
const legacySections = { safelist: 'decision', flow: 'philosophy', data: 'assets' };
function followLegacySection() {
  const id = legacySections[window.location.hash.slice(1)];
  if (id) document.getElementById(id)?.scrollIntoView();
}
window.addEventListener('hashchange', followLegacySection);
followLegacySection();

// Progressive enhancement: content remains visible without JavaScript.
const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
if ('IntersectionObserver' in window && !motionPreference.matches) {
  const reveal = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.section-intro,.section-head,.product-card,.select-feature,.lia-feature,.principles article').forEach((element) => {
    if (element.getBoundingClientRect().top > window.innerHeight) { element.classList.add('reveal-ready'); reveal.observe(element); }
  });
}
document.querySelectorAll('.film-stage video[data-src]').forEach((film) => {
  const stage = film.closest('.film-stage');
  const toggle = stage.querySelector('.film-toggle');
  const smallScreen = window.matchMedia('(max-width: 800px)');
  let userPaused = false;
  let visible = false;
  toggle.hidden = false;
  const updateButton = () => { toggle.textContent = film.paused ? toggle.dataset.play : toggle.dataset.pause; toggle.setAttribute('aria-pressed', String(!film.paused)); };
  const play = async () => {
    if (!film.getAttribute('src')) film.src = film.dataset.src;
    try { await film.play(); } catch { updateButton(); }
  };
  film.addEventListener('playing', () => { stage.classList.add('is-playing'); updateButton(); });
  film.addEventListener('pause', updateButton);
  film.addEventListener('error', () => { stage.classList.remove('is-playing'); toggle.hidden = true; });
  toggle.addEventListener('click', () => { if (film.paused) { userPaused = false; play(); } else { userPaused = true; film.pause(); } });
  const canAutoplay = () => !motionPreference.matches && !smallScreen.matches && !navigator.connection?.saveData && !userPaused && !document.hidden;
  if ('IntersectionObserver' in window) {
    new IntersectionObserver((entries) => {
      visible = entries[0].isIntersecting;
      if (!visible) film.pause(); else if (canAutoplay()) play();
    }, { threshold: 0.15 }).observe(film);
  }
  document.addEventListener('visibilitychange', () => { if (document.hidden) film.pause(); else if (visible && canAutoplay()) play(); });
  motionPreference.addEventListener('change', () => { if (motionPreference.matches) { film.pause(); stage.classList.remove('is-playing'); } });
});

// Short, one-time explanatory motion: never an endless decorative loop.
if ('IntersectionObserver' in window && !motionPreference.matches) {
  const steps = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add('in-view'); observer.unobserve(entry.target); } });
  }, { threshold: 0.5 });
  document.querySelectorAll('.motion-once').forEach((element) => steps.observe(element));
}

// AP brand system v1: approved shared stencil-cut corporate mark.
(function applyAPBrand(){
 const replace=()=>{
  document.querySelectorAll('a.brand').forEach(a=>{const img=document.createElement('img');img.src='/assets/brand/ap-holdings.svg';img.alt='AP HOLDINGS';img.width=230;img.height=33;img.className='ap-ci-logo';a.replaceChildren(img);});
  const footer=document.querySelector('.footer-map');if(footer&&!footer.querySelector('[data-brand-guide]')){const link=document.createElement('a');link.href='/ko/brand/';link.textContent='CI · BI / Brand System';link.dataset.brandGuide='true';(footer.querySelector('div')||footer).append(link);}
 };
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',replace);else replace();
})();

(function organizeAPSitemap(){
const run=()=>{
const map=document.querySelector('.footer-map');if(!map)return;
const lang=document.documentElement.lang==='ko'?'ko':'en';
const links=[...map.querySelectorAll('a')];const lia=links.find(a=>/\/products\/lia\/$/.test(a.getAttribute('href')||''));
if(lia){const group=document.createElement('div');const title=document.createElement('b');title.textContent='Entertainment';group.append(title,lia);map.append(group);}
const groups=[...map.children];const play=groups.find(g=>g.querySelector('b')?.textContent.includes('Play'));
let games=groups.find(g=>g.querySelector('b')?.textContent==='AP GAMES');
if(!games){games=document.createElement('div');const title=document.createElement('b');title.textContent='AP GAMES';games.append(title);map.append(games);}
for(const group of groups){if(group===games)continue;const title=group.querySelector('b')?.textContent||'';if(title.includes('RANKERS')){[...group.querySelectorAll('a')].forEach(a=>games.append(a));group.remove();}}
if(play){[['AP EDU',/edu\.apholdings|\/products\/cubs\/$/],['AP GAMES',/games\.apholdings|\/products\/lastwave\/$|\/products\/rgrg\/$|\/rankers\//]].forEach(([name,re])=>{let group=[...map.children].find(g=>g.querySelector('b')?.textContent===name);if(!group){group=document.createElement('div');const b=document.createElement('b');b.textContent=name;group.append(b);map.append(group);} [...play.querySelectorAll('a')].filter(a=>re.test(a.href)).forEach(a=>group.append(a));});if(!play.querySelector('a'))play.remove();}
if(![...games.querySelectorAll('a')].some(a=>a.href==='https://games.apholdings.kr/ko/play/')){const a=document.createElement('a');a.href='https://games.apholdings.kr/ko/play/';a.textContent=lang==='ko'?'로그인 · 웹 게임':'Sign in · web games';games.append(a);}
const first=map.querySelector('div');if(first&&!first.querySelector('[data-sitemap]')){const a=document.createElement('a');a.href='/ko/sitemap/';a.textContent=lang==='ko'?'전체 사이트맵':'Sitemap';a.dataset.sitemap='true';first.append(a);}
};if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
})();

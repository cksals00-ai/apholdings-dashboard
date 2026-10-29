/* AP public-site aggregate analytics v20261029b (play 추가). No cookies or persistent identifiers. */
(() => {
  if (window.__apAnalyticsLoaded) return;
  const loc=window.location, host=loc.hostname, path=loc.pathname;
  const hosts=['www.apholdings.kr','apholdings.kr','edu.apholdings.kr','games.apholdings.kr','sports.apholdings.kr','shop.apholdings.kr','ent.apholdings.kr'];
  if (!hosts.includes(host) || window.navigator.globalPrivacyControl || /(?:^|\/)(?:admin|auth|login|account|checkout|cart|submit|qna|support|analytics)(?:\/|$)/i.test(path)) return;
  if (['www.apholdings.kr','apholdings.kr'].includes(host) && path!=='/' && !/^\/(?:ko|en|ja|vi|fr|zh-cn|play)(?:\/|$)/.test(path)) return;
  window.__apAnalyticsLoaded=true;
  const params=loc.searchParams || new URL(loc.href).searchParams;
  if(params.get('ap_analytics')==='off') return;
  window.dataLayer=window.dataLayer||[];
  const gtag=function(){
    window.dataLayer.push(arguments);
    if(arguments[0]==='event' && ['page_view','courtmate_blog_arrival','ap_install_test'].includes(arguments[1]) && typeof window.fetch==='function'){
      window.fetch('https://cgijpcimixaregbpvqbf.supabase.co/functions/v1/web-count',{method:'POST',credentials:'omit',keepalive:true,referrerPolicy:'no-referrer',headers:{'Content-Type':'text/plain;charset=UTF-8'},body:JSON.stringify({host,event:arguments[1]})}).catch(()=>{});
    }
  };
  gtag('consent','default',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});
  gtag('set','ads_data_redaction',true);gtag('set','url_passthrough',false);
  let ref='';try{ref=new URL(document.referrer).origin+'/';}catch{}
  // Drop all query/hash values and page titles: these may contain names or form contents.
  const safePath=/^[a-zA-Z0-9/_\.\-]*$/.test(path)?path:'/';
  const page={page_location:loc.origin+safePath,page_referrer:ref,page_title:'AP Holdings · '+host,send_to:'G-GVD6KC9GKT'};
  gtag('js',new Date());
  gtag('config','G-GVD6KC9GKT',{send_page_view:false,allow_google_signals:false,allow_ad_personalization_signals:false,page_location:page.page_location,page_referrer:ref,page_title:page.page_title});
  const test=params.get('_ap_analytics_test')==='1';
  gtag('event',test?'ap_install_test':'page_view',page);
  if(!test && host==='sports.apholdings.kr' && params.get('utm_source')==='naver' && params.get('utm_medium')==='blog' && params.get('utm_campaign')==='courtmate_intro_20261029' && params.get('utm_content')==='224457592380') gtag('event','courtmate_blog_arrival',page);
  // 머니 머지(/play) 도착 경로: 값은 고정 목록으로만 보낸다(검색어·입력값 없음). 2026-10-29
  if(!test && ['www.apholdings.kr','apholdings.kr'].includes(host) && /^\/play\/?$/.test(path)){
    const src=(params.get('utm_source')||'').toLowerCase(), med=(params.get('utm_medium')||'').toLowerCase();
    const ch=src==='lia'?({instagram:'instagram',tiktok:'tiktok',youtube:'youtube'}[med]||'lia_other'):src==='share'?'share':src?'other':'';
    if(ch) gtag('event','money_merge_arrival_'+ch,page);
  }
  const tag=document.createElement('script');tag.async=true;tag.src='https://www.googletagmanager.com/gtag/js?id=G-GVD6KC9GKT';tag.referrerPolicy='no-referrer';document.head.appendChild(tag);
  // Visible disclosure on every measured page; no consent upgrade or cookie-writing path.
  const note=document.createElement('aside');note.setAttribute('aria-label','방문 통계 안내');note.style.cssText='font:12px/1.6 system-ui,sans-serif;padding:12px 20px;color:#657080;background:#f4f6f8;text-align:center';
  note.innerHTML='페이지 조회·소개 링크 도착 횟수를 AP 자체 집계와 Google Analytics로 확인합니다. AP 집계에는 날짜·사이트·고정 이벤트별 합계만 저장하며 IP·이름·식별자는 저장하지 않습니다. 분석·광고 쿠키와 광고 개인화는 사용하지 않으며, 페이지 주소(검색어·입력값 제외), 접속 환경·시각 등 쿠키 없는 측정 정보가 Google에 전송될 수 있습니다. 반복 조회가 포함되므로 사람 수와 다릅니다. <a href="https://www.apholdings.kr/analytics/notice.html" style="color:inherit">자세히 보기·측정 제외</a>';
  document.body.appendChild(note);
})();

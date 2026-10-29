/* AP public-site aggregate analytics v20261029. No cookies or persistent identifiers. */
(() => {
  if (window.__apAnalyticsLoaded) return;
  const loc=window.location, host=loc.hostname, path=loc.pathname;
  const hosts=['www.apholdings.kr','apholdings.kr','edu.apholdings.kr','games.apholdings.kr','sports.apholdings.kr','shop.apholdings.kr','ent.apholdings.kr'];
  if (!hosts.includes(host) || window.navigator.globalPrivacyControl || /(?:^|\/)(?:admin|auth|login|account|checkout|cart|submit|qna|support|analytics)(?:\/|$)/i.test(path)) return;
  if (['www.apholdings.kr','apholdings.kr'].includes(host) && path!=='/' && !/^\/(?:ko|en|ja|vi|fr|zh-cn)(?:\/|$)/.test(path)) return;
  window.__apAnalyticsLoaded=true;
  const params=loc.searchParams || new URL(loc.href).searchParams;
  if(params.get('ap_analytics')==='off') return;
  window.dataLayer=window.dataLayer||[];
  const gtag=function(){window.dataLayer.push(arguments);};
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
  const tag=document.createElement('script');tag.async=true;tag.src='https://www.googletagmanager.com/gtag/js?id=G-GVD6KC9GKT';tag.referrerPolicy='no-referrer';document.head.appendChild(tag);
  // Visible disclosure on every measured page; no consent upgrade or cookie-writing path.
  const note=document.createElement('aside');note.setAttribute('aria-label','방문 통계 안내');note.style.cssText='font:12px/1.6 system-ui,sans-serif;padding:12px 20px;color:#657080;background:#f4f6f8;text-align:center';
  note.innerHTML='페이지 조회 통계를 Google Analytics로 측정합니다. 분석·광고 쿠키와 광고 개인화는 사용하지 않으며, 페이지 주소(검색어·입력값 제외), 접속 환경·시각 등 쿠키 없는 측정 정보가 Google에 전송될 수 있습니다. 반복 조회가 포함되므로 사람 수와 다릅니다. <a href="https://www.apholdings.kr/analytics/notice.html" style="color:inherit">자세히 보기·측정 제외</a>';
  document.body.appendChild(note);
})();

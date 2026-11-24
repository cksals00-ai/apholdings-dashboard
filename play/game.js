/* 머니 머지 / Money Merge — AP Holdings · apholdings.kr/play
   같은 돈끼리 합쳐 10원을 빌딩·AP까지. 매일(KST) 같은 순서, 무제한 도전, 하루 최고점으로 랭킹.
   v4: 한국어/영어 자동(브라우저 언어, ?lang=ko|en, 상단 토글), 카카오 로그인, 봇/녹화용 훅 */
(function () {
'use strict';
var M = window.Matter, Engine = M.Engine, Bodies = M.Bodies, Body = M.Body, Composite = M.Composite, Events = M.Events;

/* ---------- 설정 ---------- */
var SB_URL = 'https://cxwdrlrqhxpnpepzrths.supabase.co';
var SB_KEY = 'sb_publishable_kqN8H7X5M8vt82mrmFWcVA_vg3EQBqR';
var LAUNCH = '2026-10-29';
var W = 360, H = 560, DROP_Y = 46, DANGER_Y = 92, WALL = 40;

function $(id) { return document.getElementById(id); }
var store = {
  get: function (k, d) { try { var v = localStorage.getItem('mm_' + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
  set: function (k, v) { try { localStorage.setItem('mm_' + k, JSON.stringify(v)); } catch (e) {} }
};

/* ---------- 언어 ---------- */
var LANG = (function () {
  var q = null; try { q = new URLSearchParams(location.search).get('lang'); } catch (e) {}
  if (q === 'en' || q === 'ko') { store.set('lang', q); return q; }
  var s = store.get('lang', null); if (s === 'en' || s === 'ko') return s;
  return /^ko/i.test(navigator.language || '') ? 'ko' : 'en';
})();
var STR = {
  ko: {
    title: '머니 머지 — 10원으로 빌딩까지 | AP Holdings', board: '오늘의 판 #', rankBtn: '오늘의 랭킹',
    best: '오늘 최고 ', bestNone: '오늘 최고 —', bestFirst: '오늘 첫 기록 도전 중',
    stTitle: '10원으로<br>빌딩까지', stSub: '같은 돈끼리 부딪히면 합쳐집니다.<br>금고가 넘치기 전에 최대한 키우세요.',
    how1: '밀어서 자리 잡고<br>탭하면 떨어져요', how2: '같은 돈끼리<br>합치기', how3: '매일 새 판<br>랭킹 도전',
    start: '시작하기', startAgain: '오늘 기록 깨러 가기', stNote: '오늘은 모두 같은 순서로 떨어집니다 · 횟수 무제한',
    over: '금고가 넘쳤어요!', newBest: '오늘 최고 기록 경신!', meta: '최고 단계 <b>{lv}</b> · 오늘 최고 <b>{best}</b>',
    again: '↻ 다시 하기', share: '공유하기', seeRank: '랭킹 보기',
    saving: '랭킹에 기록하는 중…', ranked: '오늘 <b>{rank}위</b> / {total}명{tier} · 연속 <b>{streak}일</b>',
    rankedSmall: '{nick} · 오늘 최고 {best} · 티어는 AP 게임 통합 등급에 반영돼요',
    saveFail: '랭킹 서버에 연결하지 못했어요.', saveFailSmall: '기록은 이 기기에 저장됐어요.',
    est: '이 점수면 오늘 <b>{rank}위</b>예요.', estNone: '랭킹에 이름을 올려보세요.', estTry: '오늘의 랭킹에 도전해 보세요.',
    loginLine: '로그인하면 바로 랭킹에 올라갑니다.', loginSmall: '3초면 끝 · 닉네임만 공개 · 연속 {streak}일 기록도 보관돼요',
    google: '구글로 랭킹 올리기', kakao: '카카오로 랭킹 올리기', googleStart: '구글로 시작하기', kakaoStart: '카카오로 시작하기',
    sheetToday: '오늘의 자산 랭킹', sheetAll: '명예의 전당', tabToday: '오늘', tabAll: '명예의 전당',
    editNick: '닉네임 바꾸기', meToday: '오늘 <b>{rank}위</b> · {score}', meNone: '오늘 기록 없음 — 한 판 해볼까요?', streak: ' · 연속 {n}일',
    meBest: '내 오늘 최고 <b>{best}</b> — 아직 랭킹에 없어요.', meLogin: '로그인하면 기록이 랭킹에 올라가요.',
    loading: '불러오는 중…', loadFail: '랭킹을 불러오지 못했어요.<br>잠시 후 다시 열어 주세요.',
    emptyToday: '오늘 첫 기록의 주인공이 되어보세요!<br>1위 자리가 비어 있어요.', emptyAll: '아직 기록이 없어요.', logout: '로그아웃',
    nickPrompt: '랭킹에 보일 닉네임 (2~12자)\nAP 게임 공용 닉네임이라 다른 AP 게임에도 같이 바뀝니다.', nickSet: '닉네임: ', nickErr: '2~12자로, 특수문자 없이 입력해 주세요',
    retry: '잠시 후 다시 시도해 주세요', loggedOut: '로그아웃했어요', posted: '랭킹 등록 완료! 오늘 {rank}위', postFail: '랭킹 등록에 실패했어요',
    copied: '결과를 복사했어요. 친구에게 붙여넣기!', copyPrompt: '복사해서 공유하세요', urlCopied: '주소를 복사했어요. 사파리·크롬에 붙여넣기!', urlPrompt: '이 주소를 사파리·크롬에서 열어 주세요',
    inTitle: '브라우저에서<br>열어 주세요', inP: '인스타그램·틱톡 안의 브라우저에서는<br>구글 로그인이 막혀 있어요.<br>사파리나 크롬으로 열면 바로 됩니다.',
    inOpen: '브라우저에서 열기', inCopy: '주소 복사', inKakao: '여기서 바로: 카카오로 시작하기', inSmall: '안 열리면 오른쪽 위 ··· 메뉴 → 「브라우저에서 열기」<br>게임 기록은 그대로 남아 있어요.', close: '닫기',
    combo: '콤보 ×', first: '첫 {lv}!', jackpot: '+1,000억 잭팟!', tapDrop: '밀어서 옮기고 · 탭하면 떨어져요',
    shareTitle: '머니 머지', shareText: '머니 머지 #{n}\n{bar}\n자산 {score} · {lv}까지!{rank}\n나보다 많이 벌 수 있어? 👉', shareRank: '\n오늘 {rank}위 / {total}명',
    foot: '매일 자정 새 판 · ', footLink: 'AP Holdings 둘러보기', statNote: '페이지 조회 통계를 Google Analytics로 측정합니다 · 안내', langBtn: 'EN',
    lv: ['10원', '50원', '100원', '500원', '천원', '오천원', '만원', '오만원', '금괴', '빌딩', 'AP'],
    face: ['10', '50', '100', '500', '1천', '5천', '1만', '5만'], tier: {}
  },
  en: {
    title: 'Money Merge — ₩10 to a Building | AP Holdings', board: 'Board #', rankBtn: "Today's ranking",
    best: "Today's best ", bestNone: "Today's best —", bestFirst: "Going for today's first record",
    stTitle: '₩10 to<br>a Building', stSub: 'Same coins merge when they touch.<br>Grow it before the vault overflows.',
    how1: 'Drag to place,<br>tap to drop', how2: 'Merge<br>same money', how3: 'New board daily,<br>climb the ranks',
    start: 'Start', startAgain: "Beat today's record", stNote: 'Same board for everyone today · unlimited tries',
    over: 'The vault overflowed!', newBest: 'New best today!', meta: "Top level <b>{lv}</b> · today's best <b>{best}</b>",
    again: '↻ Play again', share: 'Share', seeRank: 'Ranking',
    saving: 'Saving to the ranking…', ranked: 'Today <b>#{rank}</b> of {total}{tier} · <b>{streak}-day</b> streak',
    rankedSmall: "{nick} · today's best {best} · your tier counts toward your AP Games rank",
    saveFail: "Couldn't reach the ranking server.", saveFailSmall: 'Your record is saved on this device.',
    est: 'That score would be <b>#{rank}</b> today.', estNone: 'Put your name on the board.', estTry: "Take on today's ranking.",
    loginLine: 'Sign in and it goes straight to the board.', loginSmall: '3 seconds · only your nickname is shown · your {streak}-day streak is kept',
    google: 'Google — post my score', kakao: 'Kakao — post my score', googleStart: 'Continue with Google', kakaoStart: 'Continue with Kakao',
    sheetToday: "Today's wealth ranking", sheetAll: 'Hall of Fame', tabToday: 'Today', tabAll: 'All-time',
    editNick: 'Change nickname', meToday: 'Today <b>#{rank}</b> · {score}', meNone: 'No record today — play a round?', streak: ' · {n}-day streak',
    meBest: 'My best today <b>{best}</b> — not on the board yet.', meLogin: 'Sign in to put your record on the board.',
    loading: 'Loading…', loadFail: "Couldn't load the ranking.<br>Try again in a moment.",
    emptyToday: "Be today's first on the board!<br>#1 is still open.", emptyAll: 'No records yet.', logout: 'Sign out',
    nickPrompt: 'Nickname shown on the board (2–12 characters)\nShared across AP Games.', nickSet: 'Nickname: ', nickErr: 'Use 2–12 characters, no special symbols',
    retry: 'Please try again in a moment', loggedOut: 'Signed out', posted: "Posted! You're #{rank} today", postFail: "Couldn't post your score",
    copied: 'Copied! Paste it to a friend', copyPrompt: 'Copy and share', urlCopied: 'Link copied — paste it into Safari or Chrome', urlPrompt: 'Open this link in Safari or Chrome',
    inTitle: 'Open in your<br>browser', inP: 'Google sign-in is blocked inside the<br>Instagram / TikTok browser.<br>Open in Safari or Chrome and it works.',
    inOpen: 'Open in browser', inCopy: 'Copy link', inKakao: 'Or right here: continue with Kakao', inSmall: "If nothing opens: tap ··· (top right) → “Open in browser”.<br>Your game record stays.", close: 'Close',
    combo: 'Combo ×', first: 'First {lv}!', jackpot: '+₩100B JACKPOT!', tapDrop: 'Drag to move · tap to drop',
    shareTitle: 'Money Merge', shareText: 'Money Merge #{n}\n{bar}\nWealth {score} · reached {lv}!{rank}\nCan you make more than me? 👉', shareRank: '\nToday #{rank} of {total}',
    foot: 'New board at midnight KST · ', footLink: 'Explore AP Holdings', statNote: 'Page views are measured with Google Analytics · details', langBtn: 'KO',
    lv: ['₩10', '₩50', '₩100', '₩500', '₩1,000', '₩5,000', '₩10,000', '₩50,000', 'Gold bar', 'Building', 'AP'],
    face: ['10', '50', '100', '500', '1K', '5K', '10K', '50K'], tier: { '새내기': 'Rookie', '숙련': 'Skilled', '고수': 'Expert', '달인': 'Master', '명인': 'Grandmaster' }
  }
};
function t(k, v) { var s = STR[LANG][k]; if (s == null) s = STR.ko[k]; if (v) for (var key in v) s = s.split('{' + key + '}').join(v[key]); return s; }
function tierName(x) { return x ? (STR[LANG].tier[x] || x) : ''; }

// 단계: 이름, 반지름, 만들었을 때 점수(원), 색
var LV = [
  { r: 15, v: 10,          c: ['#E9A271', '#B9693B', '#7A3E1C'], ink: '#4A230C', coin: 1 },
  { r: 21, v: 50,          c: ['#F1F3F5', '#B9C0C8', '#6E7781'], ink: '#3B424A', coin: 1 },
  { r: 27, v: 100,         c: ['#F4F6F8', '#AEB6BF', '#5F6973'], ink: '#323A43', coin: 1 },
  { r: 34, v: 500,         c: ['#FFFFFF', '#C3CAD2', '#707A85'], ink: '#2A323B', coin: 1 },
  { r: 41, v: 1000,        c: ['#9CC9F0', '#4C8CC4', '#244F78'], ink: '#fff' },
  { r: 49, v: 5000,        c: ['#FFC48A', '#E07B35', '#8E4313'], ink: '#fff' },
  { r: 57, v: 10000,       c: ['#A8E0A3', '#4E9E58', '#245A2D'], ink: '#fff' },
  { r: 66, v: 50000,       c: ['#FFE38A', '#E3A62A', '#8C5A00'], ink: '#4A2E00' },
  { r: 75, v: 1000000,     c: ['#FFF0A6', '#F5C542', '#A86F00'], ink: '#5A3A00', icon: 'gold' },
  { r: 85, v: 100000000,   c: ['#5D7BA6', '#2A4268', '#0E1A2B'], ink: '#fff', icon: 'bld' },
  { r: 96, v: 10000000000, c: ['#FFFFFF', '#E9E4D8', '#9C9384'], ink: '#0E1A2B', icon: 'ap' }
];
for (var li = 0; li < LV.length; li++) { LV[li].k = STR[LANG].lv[li]; LV[li].t = li < 8 ? STR[LANG].face[li] : (li === 8 ? '금괴' : li === 9 ? '빌딩' : 'AP'); }
var DROP_W = [32, 26, 20, 14, 8]; // 0~4단계만 떨어짐

/* ---------- 유틸 ---------- */
function kstDay(tm) { return new Date((tm || Date.now()) + 9 * 3600e3).toISOString().slice(0, 10); }
function dayNo(d) { return Math.round((Date.parse(d) - Date.parse(LAUNCH)) / 864e5) + 1; }
function won(n) {
  n = Math.floor(n);
  if (LANG === 'en') {
    if (n >= 1e9) return '₩' + (n / 1e9).toFixed(n % 1e9 ? 1 : 0) + 'B';
    if (n >= 1e6) return '₩' + (n / 1e6).toFixed(n % 1e6 ? 1 : 0) + 'M';
    return '₩' + n.toLocaleString('en-US');
  }
  if (n >= 1e8) { var e = Math.floor(n / 1e8), m = Math.floor((n % 1e8) / 1e4); return e.toLocaleString() + '억' + (m ? ' ' + m.toLocaleString() + '만' : '') + '원'; }
  if (n >= 1e4) { var mm = Math.floor(n / 1e4), r = n % 1e4; return mm.toLocaleString() + '만' + (r ? ' ' + r.toLocaleString() : '') + '원'; }
  return n.toLocaleString() + '원';
}
function wonShort(n) {
  if (LANG === 'en') {
    if (n >= 1e9) return (n / 1e9).toFixed(1) + 'B';
    if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
    if (n >= 1e4) return Math.round(n / 1e3) + 'K';
    return n.toLocaleString('en-US');
  }
  if (n >= 1e8) return (Math.floor(n / 1e7) / 10).toLocaleString() + '억';
  if (n >= 1e4) return Math.floor(n / 1e4).toLocaleString() + '만';
  return n.toLocaleString();
}
function hashStr(s) { var h = 1779033703 ^ s.length; for (var i = 0; i < s.length; i++) { h = Math.imul(h ^ s.charCodeAt(i), 3432918353); h = h << 13 | h >>> 19; } return h >>> 0; }
function rng(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var tt = Math.imul(seed ^ seed >>> 15, 1 | seed); tt = tt + Math.imul(tt ^ tt >>> 7, 61 | tt) ^ tt; return ((tt ^ tt >>> 14) >>> 0) / 4294967296; }; }
function toast(msg) { var el = $('toast'); el.textContent = msg; el.classList.add('on'); clearTimeout(toast._t); toast._t = setTimeout(function () { el.classList.remove('on'); }, 2200); }
/* 통계: 홈페이지 공용 ap-analytics(쿠키 없음)가 떠 있으면 GA4로 간다. 개인 식별값은 보내지 않는다. */
function ga() { try { (window.dataLayer = window.dataLayer || []).push(arguments); } catch (e) {} }
function scoreBucket(n) { return n >= 1e8 ? '1억+' : n >= 1e7 ? '1천만+' : n >= 1e6 ? '100만+' : n >= 1e5 ? '10만+' : n >= 1e4 ? '1만+' : '1만 미만'; }
// 인스타그램·틱톡·페이스북·카톡 등 앱 안 브라우저 — 구글 로그인이 403(disallowed_useragent)으로 막힌다 (카카오는 됨)
var IN_APP = /Instagram|FBAN|FBAV|FB_IAB|TikTok|musical_ly|Bytedance|KAKAOTALK|\bLine\//i.test(navigator.userAgent);
var IS_IOS = /iPhone|iPad|iPod/i.test(navigator.userAgent), IS_ANDROID = /Android/i.test(navigator.userAgent);
function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

/* ---------- 그리기 ---------- */
function drawItem(ctx, lv, x, y, r, ang, alpha) {
  var L = LV[lv];
  ctx.save(); ctx.translate(x, y); if (ang) ctx.rotate(ang); if (alpha != null) ctx.globalAlpha = alpha;
  var g = ctx.createRadialGradient(-r * .35, -r * .4, r * .1, 0, 0, r);
  g.addColorStop(0, L.c[0]); g.addColorStop(.6, L.c[1]); g.addColorStop(1, L.c[2]);
  ctx.beginPath(); ctx.arc(0, 0, r, 0, Math.PI * 2); ctx.fillStyle = g; ctx.fill();
  ctx.lineWidth = Math.max(1.5, r * .09); ctx.strokeStyle = L.c[2]; ctx.stroke();
  ctx.beginPath(); ctx.arc(0, 0, r * .8, 0, Math.PI * 2); ctx.lineWidth = Math.max(1, r * .04);
  ctx.strokeStyle = L.coin ? 'rgba(0,0,0,.18)' : 'rgba(255,255,255,.35)'; if (!L.coin) ctx.setLineDash([r * .12, r * .08]); ctx.stroke(); ctx.setLineDash([]);
  ctx.beginPath(); ctx.ellipse(-r * .3, -r * .42, r * .38, r * .18, -.5, 0, Math.PI * 2); ctx.fillStyle = 'rgba(255,255,255,.28)'; ctx.fill();
  ctx.fillStyle = L.ink;
  if (L.icon === 'gold') {
    var w = r * .95, h = r * .42;
    ctx.beginPath(); ctx.moveTo(-w / 2, h / 2); ctx.lineTo(w / 2, h / 2); ctx.lineTo(w / 2 - h * .5, -h / 2); ctx.lineTo(-w / 2 + h * .5, -h / 2); ctx.closePath();
    ctx.fillStyle = '#C88A00'; ctx.fill(); ctx.lineWidth = r * .05; ctx.strokeStyle = '#5A3A00'; ctx.stroke();
    ctx.fillStyle = '#FFE680'; ctx.fillRect(-w / 2 + h * .55, -h / 2 + r * .05, w * .4, r * .06);
    ctx.fillStyle = L.ink; ctx.font = '900 ' + (r * .3) + 'px "Noto Sans KR",sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('GOLD', 0, h * .05 + r * .02);
  } else if (L.icon === 'bld') {
    ctx.fillStyle = '#F5C542';
    var bw = r * .34;
    ctx.fillRect(-bw * 1.5, -r * .2, bw, r * .72); ctx.fillRect(-bw * .45, -r * .62, bw * 1.1, r * 1.14); ctx.fillRect(bw * .75, -r * .05, bw * .85, r * .57);
    ctx.fillStyle = '#2A4268';
    for (var i = 0; i < 5; i++) for (var j = 0; j < 2; j++) ctx.fillRect(-bw * .3 + j * bw * .45, -r * .5 + i * r * .2, bw * .28, r * .1);
    for (i = 0; i < 3; i++) { ctx.fillRect(-bw * 1.32, -r * .08 + i * r * .2, bw * .6, r * .09); ctx.fillRect(bw * .9, r * .06 + i * r * .15, bw * .55, r * .07); }
  } else if (L.icon === 'ap') {
    ctx.font = '900 ' + (r * .78) + 'px "Noto Sans KR",sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('AP', 0, r * .04);
    ctx.font = '700 ' + (r * .14) + 'px "Noto Sans KR",sans-serif'; ctx.fillText('HOLDINGS', 0, r * .5);
  } else {
    var fs = L.t.length >= 3 ? r * .62 : r * .72;
    ctx.font = '900 ' + fs + 'px "Noto Sans KR",sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(L.t, 0, r * .05);
  }
  ctx.restore();
}
function iconCanvas(cvs, lv, locked) {
  var c = cvs.getContext('2d'), s = cvs.width; c.clearRect(0, 0, s, s);
  if (locked) { c.beginPath(); c.arc(s / 2, s / 2, s * .4, 0, 7); c.fillStyle = 'rgba(255,255,255,.06)'; c.fill(); c.fillStyle = 'rgba(255,255,255,.3)'; c.font = '900 ' + s * .4 + 'px sans-serif'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('?', s / 2, s / 2 + s * .02); return; }
  drawItem(c, lv, s / 2, s / 2, s * .44);
}

/* ---------- 소리 ---------- */
var AC = null, muted = store.get('mute', false);
function tone(freq, dur, type, vol, when) {
  if (muted) return;
  try {
    AC = AC || new (window.AudioContext || window.webkitAudioContext)();
    var tm = AC.currentTime + (when || 0), o = AC.createOscillator(), g = AC.createGain();
    o.type = type || 'sine'; o.frequency.setValueAtTime(freq, tm); o.frequency.exponentialRampToValueAtTime(freq * 1.5, tm + dur);
    g.gain.setValueAtTime(vol || .15, tm); g.gain.exponentialRampToValueAtTime(.0001, tm + dur);
    o.connect(g); g.connect(AC.destination); o.start(tm); o.stop(tm + dur + .02);
  } catch (e) {}
}
function sMerge(lv, combo) {
  var base = 520 + lv * 60 + Math.min(combo, 8) * 40;
  tone(base, .12, 'triangle', .16); tone(base * 1.5, .16, 'sine', .1, .05);
  if (lv >= 7) { tone(base * 2, .3, 'sine', .1, .1); tone(base * 2.5, .4, 'sine', .08, .18); }
}
function sDrop() { tone(300, .06, 'sine', .07); }
function sOver() { tone(330, .25, 'sawtooth', .08); tone(247, .35, 'sawtooth', .08, .2); tone(196, .5, 'sawtooth', .08, .45); }
function setMuteIcon() {
  $('mute').innerHTML = muted
    ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 5 6 9H2v6h4l5 4V5z"/><path d="m23 9-6 6M17 9l6 6"/></svg>'
    : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 5 6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/></svg>';
}

/* ---------- 상태 ---------- */
var cv = $('cv'), ctx = cv.getContext('2d'), scale = 1, dpr = 1;
var engine, world, items = [], particles = [], floats = [];
var state = 'ready', score = 0, drops = 0, maxLv = 0, combo = 0, lastMerge = 0, startAt = 0, overT = 0, shake = 0;
var aimX = W / 2, aimTarget = W / 2, cur = 0, nxt = 0, canDropAt = 0, R = null, playDay = kstDay();
// 조작: 먼저 자리를 잡고(탭·드래그·마우스 이동 → 동전이 미끄러져 감), 그 자리를 다시 탭/클릭하면 떨어진다
var lastPtr = 'mouse', ptrStart = null, previewPop = 1, hintCount = store.get('hint', 0);
var today = kstDay(), dex = store.get('dex', -1);
var eventLog = []; // 봇·녹화용: 합치기/종료 시각

function bestToday() { var b = store.get('best', {}); return b.day === today ? b : null; }

function resize() {
  var st = $('stage'), aw = st.clientWidth, ah = st.clientHeight;
  scale = Math.min(aw / W, ah / H); dpr = Math.min(window.devicePixelRatio || 1, 2.5);
  cv.style.width = (W * scale) + 'px'; cv.style.height = (H * scale) + 'px';
  cv.width = Math.round(W * scale * dpr); cv.height = Math.round(H * scale * dpr);
}

function pickLv() { var tot = 0, i; for (i = 0; i < DROP_W.length; i++) tot += DROP_W[i]; var x = R() * tot; for (i = 0; i < DROP_W.length; i++) { x -= DROP_W[i]; if (x < 0) return i; } return 0; }

function newGame() {
  today = kstDay(); playDay = today;
  if (engine) { Composite.clear(world, false); Engine.clear(engine); }
  engine = Engine.create({ gravity: { y: 1.25 } }); world = engine.world;
  engine.positionIterations = 8; engine.velocityIterations = 6;
  var opt = { isStatic: true, friction: .3, label: 'wall' };
  Composite.add(world, [
    Bodies.rectangle(W / 2, H - 3 + WALL / 2, W + WALL * 2, WALL, opt),
    Bodies.rectangle(-WALL / 2, H / 2 - 200, WALL, H + 400, opt),
    Bodies.rectangle(W + WALL / 2, H / 2 - 200, WALL, H + 400, opt)
  ]);
  Events.on(engine, 'collisionStart', onCollide);
  Events.on(engine, 'collisionActive', onCollide);
  items = []; particles = []; floats = []; mergeQ = []; eventLog = [];
  R = rng(hashStr('money-merge:' + today));
  score = 0; drops = 0; maxLv = 0; combo = 0; overT = 0; shake = 0;
  cur = pickLv(); nxt = pickLv(); canDropAt = 0; startAt = performance.now();
  state = 'play';
  $('dayNo').textContent = t('board') + dayNo(today);
  updHud(); drawNext();
}

function makeItem(lv, x, y) {
  var L = LV[lv];
  var b = Bodies.circle(x, y, L.r, { restitution: .1, friction: .06, frictionStatic: .35, frictionAir: .004, density: .001 + lv * .0002, label: 'item', slop: .02 });
  b.lv = lv; b.born = performance.now(); b.pop = 1;
  Composite.add(world, b); items.push(b);
  return b;
}

var mergeQ = [];
function onCollide(e) {
  for (var i = 0; i < e.pairs.length; i++) {
    var a = e.pairs[i].bodyA, b = e.pairs[i].bodyB;
    if (a.label === 'item' && b.label === 'item' && a.lv === b.lv && !a.dead && !b.dead) {
      a.dead = b.dead = true; mergeQ.push([a, b]);
    }
  }
}

function removeItem(b) { Composite.remove(world, b); var i = items.indexOf(b); if (i >= 0) items.splice(i, 1); }

function processMerges() {
  var now = performance.now();
  for (var i = 0; i < mergeQ.length; i++) {
    var a = mergeQ[i][0], b = mergeQ[i][1], lv = a.lv;
    var x = (a.position.x + b.position.x) / 2, y = (a.position.y + b.position.y) / 2;
    removeItem(a); removeItem(b);
    combo = (now - lastMerge < 900) ? combo + 1 : 1; lastMerge = now;
    var gain, nl = lv + 1;
    if (nl >= LV.length) { // AP + AP → 대박
      gain = 100000000000; burst(x, y, '#F5C542', 60); shake = 18;
      floats.push({ x: x, y: y, t: t('jackpot'), life: 1.6, big: 1 });
    } else {
      var nb = makeItem(nl, x, Math.min(y, H - LV[nl].r));
      nb.pop = .55; Body.setVelocity(nb, { x: 0, y: -1.2 });
      gain = LV[nl].v;
      if (nl > maxLv) maxLv = nl;
      if (nl > dex) { dex = nl; store.set('dex', dex); buildDex(); if (nl >= 6) floats.push({ x: W / 2, y: H * .35, t: t('first', { lv: LV[nl].k }), life: 1.4, big: 1 }); }
      burst(x, y, LV[nl].c[1], 10 + nl * 3);
      if (nl >= 7) shake = Math.min(14, 4 + nl);
    }
    var bonus = combo > 1 ? Math.floor(gain * .1 * (combo - 1)) : 0;
    score += gain + bonus;
    floats.push({ x: x, y: y - 10, t: '+' + wonShort(gain + bonus), life: 1 });
    eventLog.push({ t: Math.round(now - startAt), e: 'merge', lv: nl, combo: combo, score: score });
    sMerge(lv, combo);
    if (navigator.vibrate && lv >= 4) try { navigator.vibrate(lv >= 7 ? 25 : 8); } catch (e2) {}
    if (combo >= 2) showCombo(combo);
  }
  if (mergeQ.length) updHud();
  mergeQ = [];
}

function burst(x, y, color, n) {
  for (var i = 0; i < n; i++) {
    var a = Math.random() * Math.PI * 2, s = 1 + Math.random() * 4;
    particles.push({ x: x, y: y, vx: Math.cos(a) * s, vy: Math.sin(a) * s - 1, life: 1, c: Math.random() < .3 ? '#fff' : color, r: 1.5 + Math.random() * 2.5 });
  }
}
var comboT;
function showCombo(n) {
  var el = $('combo'); el.textContent = t('combo') + n; el.classList.add('on');
  clearTimeout(comboT); comboT = setTimeout(function () { el.classList.remove('on'); }, 700);
}

function drop() {
  if (state !== 'play') return;
  var now = performance.now(); if (now < canDropAt) return;
  var r = LV[cur].r, x = Math.max(r + 1, Math.min(W - r - 1, aimX));
  makeItem(cur, x, DROP_Y);
  drops++; sDrop();
  cur = nxt; nxt = pickLv(); canDropAt = now + 420; previewPop = 0;
  if (lastPtr !== 'mouse' && hintCount < 3) { hintCount++; store.set('hint', hintCount); }
  drawNext();
}
function clampAim(x) { var r = LV[cur].r; return Math.max(r + 1, Math.min(W - r - 1, x)); }

function updHud() {
  $('score').textContent = won(score);
  var b = bestToday();
  $('best').textContent = b ? t('best') + won(Math.max(b.score, score)) : (score ? t('bestFirst') : t('bestNone'));
}
function drawNext() { iconCanvas($('nextCv'), nxt); }

function buildDex() {
  var el = $('dex'); el.innerHTML = '';
  for (var i = 0; i < LV.length; i++) {
    var c = document.createElement('canvas'); c.width = c.height = 64; c.title = i <= dex ? LV[i].k : '???';
    iconCanvas(c, i, i > dex && i > 4); el.appendChild(c);
  }
}

/* ---------- 루프 ---------- */
var acc = 0, last = 0;
function loop(tm) {
  requestAnimationFrame(loop);
  if (!last) last = tm; var dt = Math.min(50, tm - last); last = tm;
  if (state === 'play') {
    acc += dt;
    while (acc >= 1000 / 60) { Engine.update(engine, 1000 / 60); processMerges(); acc -= 1000 / 60; }
    checkOver(dt);
  }
  render(dt);
}

function checkOver(dt) {
  var now = performance.now(), danger = false;
  for (var i = 0; i < items.length; i++) {
    var b = items[i];
    if (now - b.born > 1200 && b.position.y - LV[b.lv].r < DANGER_Y) { danger = true; break; }
  }
  overT = danger ? overT + dt : Math.max(0, overT - dt * 2);
  if (overT > 1800) gameOver();
}

function render(dt) {
  var c = ctx, now = performance.now();
  c.setTransform(dpr * scale, 0, 0, dpr * scale, 0, 0);
  c.clearRect(0, 0, W, H);
  var sx = 0, sy = 0;
  if (shake > 0) { sx = (Math.random() - .5) * shake; sy = (Math.random() - .5) * shake; shake *= .88; if (shake < .3) shake = 0; }
  c.save(); c.translate(sx, sy);
  var g = c.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#1A2E4C'); g.addColorStop(1, '#13233A');
  c.fillStyle = g; c.fillRect(0, 0, W, H);
  c.strokeStyle = 'rgba(255,255,255,.035)'; c.lineWidth = 1;
  for (var y = 40; y < H; y += 40) { c.beginPath(); c.moveTo(0, y); c.lineTo(W, y); c.stroke(); }
  var warn = Math.min(1, overT / 1800);
  var nearTop = items.some(function (b) { return now - b.born > 1200 && b.position.y - LV[b.lv].r < DANGER_Y + 50; });
  c.setLineDash([8, 7]); c.lineWidth = 2;
  c.strokeStyle = warn > 0 ? 'rgba(255,90,95,' + (.5 + .5 * Math.sin(now / 80)) + ')' : (nearTop ? 'rgba(255,90,95,.55)' : 'rgba(255,255,255,.16)');
  c.beginPath(); c.moveTo(0, DANGER_Y); c.lineTo(W, DANGER_Y); c.stroke(); c.setLineDash([]);
  if (warn > 0) { c.fillStyle = 'rgba(255,90,95,' + warn * .18 + ')'; c.fillRect(0, 0, W, DANGER_Y); }
  if (state === 'play') {
    var tx = clampAim(aimTarget);
    aimX += (tx - aimX) * Math.min(1, dt / 50);
    if (Math.abs(tx - aimX) < .5) aimX = tx;
    var settled = Math.abs(tx - aimX) < 1.5;
    if (previewPop < 1) previewPop = Math.min(1, previewPop + dt / 160);
    var r = LV[cur].r, ax = clampAim(aimX), ready = now >= canDropAt, pr = r * (.6 + .4 * previewPop);
    c.strokeStyle = 'rgba(255,255,255,.14)'; c.lineWidth = 2; c.setLineDash([3, 6]);
    c.beginPath(); c.moveTo(ax, DROP_Y + r); c.lineTo(ax, H); c.stroke(); c.setLineDash([]);
    drawItem(c, cur, ax, DROP_Y, pr, 0, (ready ? 1 : .45) * (.4 + .6 * previewPop));
    if (lastPtr !== 'mouse' && settled && ready) {
      var pulse = .5 + .5 * Math.sin(now / 160), ay = DROP_Y + r + 10 + pulse * 4;
      c.fillStyle = 'rgba(245,197,66,' + (.55 + .35 * pulse) + ')';
      c.beginPath(); c.moveTo(ax - 7, ay); c.lineTo(ax + 7, ay); c.lineTo(ax, ay + 8); c.closePath(); c.fill();
      if (hintCount < 3) { c.font = '700 12px "Noto Sans KR",sans-serif'; c.textAlign = 'center'; c.textBaseline = 'top'; c.fillText(t('tapDrop'), W / 2, ay + 12); }
    }
  }
  for (var i = 0; i < items.length; i++) {
    var b = items[i], L = LV[b.lv];
    if (b.pop < 1) b.pop = Math.min(1, b.pop + dt / 130);
    var pr2 = L.r * (b.pop < 1 ? b.pop * (1 + .12 * Math.sin(b.pop * Math.PI)) : 1);
    drawItem(c, b.lv, b.position.x, b.position.y, pr2, b.angle);
  }
  for (i = particles.length - 1; i >= 0; i--) {
    var p = particles[i]; p.x += p.vx; p.y += p.vy; p.vy += .12; p.life -= dt / 600;
    if (p.life <= 0) { particles.splice(i, 1); continue; }
    c.globalAlpha = p.life; c.fillStyle = p.c; c.beginPath(); c.arc(p.x, p.y, p.r, 0, 7); c.fill();
  }
  c.globalAlpha = 1;
  c.textAlign = 'center'; c.textBaseline = 'middle';
  for (i = floats.length - 1; i >= 0; i--) {
    var f = floats[i]; f.life -= dt / (f.big ? 1400 : 900); f.y -= f.big ? .3 : .6;
    if (f.life <= 0) { floats.splice(i, 1); continue; }
    c.globalAlpha = Math.min(1, f.life * 2);
    c.font = '900 ' + (f.big ? 26 : 15) + 'px "Noto Sans KR",sans-serif';
    c.lineWidth = 4; c.strokeStyle = 'rgba(0,0,0,.55)'; c.strokeText(f.t, f.x, f.y);
    c.fillStyle = f.big ? '#F5C542' : '#fff'; c.fillText(f.t, f.x, f.y);
  }
  c.globalAlpha = 1;
  c.restore();
}

/* ---------- 입력 ---------- */
function toX(clientX) { var rc = cv.getBoundingClientRect(); return (clientX - rc.left) / rc.width * W; }
/* 마우스: 움직이면 동전이 따라오고, 클릭하면 떨어짐.
   터치·펜(한 손 기준): 아무 데나 대고 밀면 동전이 「지금 자리에서 민 만큼」 움직이고(손가락 위치로 점프하지 않음),
   밀지 않고 탭하면 그 자리에 떨어짐. */
var DRAG_SENS = 1.4; // 손가락 1px → 동전 1.4 (엄지 반경으로 판 끝까지 닿게)
cv.addEventListener('pointerdown', function (e) {
  lastPtr = e.pointerType || 'mouse';
  ptrStart = { x: e.clientX, y: e.clientY, drag: false, baseAim: clampAim(aimTarget), startGX: toX(e.clientX) };
  try { cv.setPointerCapture(e.pointerId); } catch (x2) {}
});
cv.addEventListener('pointermove', function (e) {
  var mouse = (e.pointerType || 'mouse') === 'mouse';
  if (mouse) { if (!ptrStart && e.buttons) return; aimTarget = toX(e.clientX); return; }
  if (!ptrStart) return;
  if (!ptrStart.drag && Math.hypot(e.clientX - ptrStart.x, e.clientY - ptrStart.y) > 8) ptrStart.drag = true;
  if (ptrStart.drag) aimTarget = clampAim(ptrStart.baseAim + (toX(e.clientX) - ptrStart.startGX) * DRAG_SENS);
});
cv.addEventListener('pointerup', function (e) {
  if (!ptrStart) return;
  var s = ptrStart, x = toX(e.clientX); ptrStart = null;
  if ((e.pointerType || 'mouse') === 'mouse') { aimTarget = x; aimX = clampAim(x); drop(); return; }
  if (s.drag) { aimTarget = clampAim(s.baseAim + (x - s.startGX) * DRAG_SENS); return; }   // 밀기 끝 → 그 자리에 둠
  aimTarget = aimX; drop();                                                                  // 탭 → 지금 자리에 떨어짐
});
cv.addEventListener('pointercancel', function () { ptrStart = null; });
var keys = {};
window.addEventListener('keydown', function (e) {
  if (e.target.tagName === 'INPUT') return;
  if (e.code === 'ArrowLeft' || e.code === 'KeyA') { keys.l = 1; e.preventDefault(); }
  if (e.code === 'ArrowRight' || e.code === 'KeyD') { keys.r = 1; e.preventDefault(); }
  if (e.code === 'Space' || e.code === 'Enter' || e.code === 'ArrowDown') {
    e.preventDefault();
    if (state === 'play') drop(); else if (state === 'ready' || state === 'over') start();
  }
  if (e.code === 'KeyR' && state === 'over') start();
});
window.addEventListener('keyup', function (e) {
  if (e.code === 'ArrowLeft' || e.code === 'KeyA') keys.l = 0;
  if (e.code === 'ArrowRight' || e.code === 'KeyD') keys.r = 0;
});
setInterval(function () { if (keys.l) { aimTarget = Math.max(0, aimTarget - 6); lastPtr = 'mouse'; } if (keys.r) { aimTarget = Math.min(W, aimTarget + 6); lastPtr = 'mouse'; } }, 16);

/* ---------- 시작·종료 ---------- */
function start() {
  $('ovStart').classList.remove('on'); $('ovOver').classList.remove('on');
  newGame();
  plays = store.get('plays', 0) + 1; store.set('plays', plays);
  ga('event', 'mm_start', { logged_in: user ? 1 : 0, lang: LANG });
}
var plays = store.get('plays', 0);

var lastResult = null;
function gameOver() {
  state = 'over'; sOver();
  var ms = Math.round(performance.now() - startAt);
  var b = bestToday(), isBest = !b || score > b.score;
  if (isBest) store.set('best', { day: playDay, score: score, top: maxLv });
  markPlayed(playDay);
  lastResult = { day: playDay, score: score, top: maxLv, drops: drops, ms: ms };
  eventLog.push({ t: ms, e: 'over', score: score, top: maxLv });
  $('ovTitle').textContent = isBest && score > 0 && b ? t('newBest') : t('over');
  $('ovScore').textContent = won(score);
  $('ovMeta').innerHTML = t('meta', { lv: LV[maxLv].k, best: won(Math.max(score, b ? b.score : 0)) });
  $('ovRank').innerHTML = '';
  setTimeout(function () { $('ovOver').classList.add('on'); }, 500);
  updHud();
  ga('event', 'mm_game_over', { score_bucket: scoreBucket(score), top_level: maxLv, drops: drops, logged_in: user ? 1 : 0, lang: LANG });
  afterGame(lastResult, isBest);
}

function markPlayed(d) {
  var s = store.get('streak', { last: null, n: 0 });
  if (s.last === d) return;
  var y = kstDay(Date.parse(d + 'T12:00:00+09:00') - 864e5);
  s.n = s.last === y ? s.n + 1 : 1; s.last = d; store.set('streak', s);
}
function localStreak() { var s = store.get('streak', { last: null, n: 0 }); var y = kstDay(Date.now() - 864e5); return (s.last === today || s.last === y) ? s.n : 0; }

/* ---------- 랭킹·로그인 ---------- */
var sb = null, user = null, me = null, board = { today: null, all: null }, tab = 'today';
try {
  sb = window.supabase.createClient(SB_URL, SB_KEY, { auth: { persistSession: true, detectSessionInUrl: true, flowType: 'pkce', storageKey: 'mm-auth' } });
} catch (e) { sb = null; }

function login(provider) {
  provider = provider || 'google';
  if (!sb) return toast(t('retry'));
  if (lastResult) store.set('pending', lastResult);
  if (IN_APP && provider === 'google') { ga('event', 'mm_login_blocked_inapp'); $('ovInapp').classList.add('on'); return; }
  ga('event', 'mm_login_click', { provider: provider });
  sb.auth.signInWithOAuth({ provider: provider, options: { redirectTo: location.origin + '/play/' + (LANG === 'en' ? '?lang=en' : '') } });
}
/* 앱 안 브라우저 → 기본 브라우저로 열기 (안드로이드: 크롬 intent, iOS: x-safari 스킴, 안 되면 주소 복사) */
function openInBrowser() {
  var url = 'https://www.apholdings.kr/play/' + (LANG === 'en' ? '?lang=en' : '');
  if (IS_ANDROID) { location.href = 'intent://www.apholdings.kr/play/' + (LANG === 'en' ? '?lang=en' : '') + '#Intent;scheme=https;package=com.android.chrome;S.browser_fallback_url=' + encodeURIComponent(url) + ';end'; return; }
  if (IS_IOS) { location.href = 'x-safari-' + url; setTimeout(function () { copyUrl(url); }, 800); return; }
  copyUrl(url);
}
function copyUrl(url) {
  (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () { toast(t('urlCopied')); })
    .catch(function () { prompt(t('urlPrompt'), url); });
}
function logout() { if (sb) sb.auth.signOut().then(function () { user = null; me = null; renderSheets(); toast(t('loggedOut')); }); }

function rpc(name, args) {
  if (!sb) return Promise.reject(new Error('no sb'));
  return sb.rpc(name, args || {}).then(function (r) { if (r.error) throw r.error; return r.data; });
}
function loadBoard() {
  var d = kstDay();
  var p1 = rpc('coin_board', { p_day: d, p_limit: 100 }).then(function (x) { board.today = x || []; }).catch(function () { board.today = board.today || 'err'; });
  var p2 = rpc('coin_board_all', { p_limit: 100 }).then(function (x) { board.all = x || []; }).catch(function () { board.all = board.all || 'err'; });
  return Promise.all([p1, p2]).then(renderSheets);
}
function loadMe() {
  if (!user) { me = null; return Promise.resolve(); }
  return rpc('coin_me').then(function (x) { me = x; }).catch(function () { me = null; });
}
function submit(res) {
  return rpc('coin_submit', { p_day: res.day, p_score: res.score, p_top: res.top, p_drops: res.drops, p_ms: res.ms });
}

function estRank(sc) {
  var l = board.today; if (!Array.isArray(l)) return null;
  var above = l.filter(function (r) { return Number(r.score) > sc && !r.is_me; }).length;
  if (l.length >= 100 && above >= 100) return null;
  return above + 1;
}

var GICON = '<svg viewBox="0 0 48 48"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>';
var KICON = '<svg viewBox="0 0 24 24"><path fill="#191919" d="M12 3C6.5 3 2 6.5 2 10.8c0 2.7 1.8 5.1 4.5 6.5l-.9 3.4c-.1.3.2.5.5.3l4-2.7c.6.1 1.2.1 1.9.1 5.5 0 10-3.5 10-7.8S17.5 3 12 3z"/></svg>';
function loginButtons(cls, big) {
  var g = '<button class="btn white ' + cls + '" data-p="google">' + GICON + (big ? t('google') : t('googleStart')) + '</button>';
  var k = '<button class="btn kakao ' + cls + '" data-p="kakao">' + KICON + (big ? t('kakao') : t('kakaoStart')) + '</button>';
  return LANG === 'ko' ? k + g : g + k;
}
function bindLogin(root) { root.querySelectorAll('button[data-p]').forEach(function (b) { b.onclick = function () { login(b.dataset.p); }; }); }

function afterGame(res, isBest) {
  var box = $('ovRank');
  if (user) {
    box.innerHTML = '<div class="ranknote"><p>' + t('saving') + '</p></div>';
    submit(res).then(function (r) {
      box.innerHTML = '<div class="ranknote"><p>' + t('ranked', { rank: r.rank, total: r.total, tier: r.tier ? ' · <b>' + esc(tierName(r.tier)) + '</b>' : '', streak: r.streak }) + '</p><small>' + t('rankedSmall', { nick: esc(r.nickname), best: won(r.best) }) + '</small></div>';
      lastResult.rank = r.rank; lastResult.total = r.total;
      ga('event', 'mm_rank_submit', { rank: r.rank, streak: r.streak });
      loadMe().then(loadBoard);
    }).catch(function () { box.innerHTML = '<div class="ranknote"><p>' + t('saveFail') + '</p><small>' + t('saveFailSmall') + '</small></div>'; });
  } else {
    var tryRender = function () {
      var er = res.score > 0 ? estRank(res.score) : null;
      var line = er ? t('est', { rank: er }) : (Array.isArray(board.today) ? t('estNone') : t('estTry'));
      box.innerHTML = '<div class="ranknote"><p>' + line + '<br>' + t('loginLine') + '</p><small>' + t('loginSmall', { streak: Math.max(1, localStreak()) }) + '</small></div>' + loginButtons('ovLogin', true);
      bindLogin(box);
    };
    tryRender(); loadBoard().then(tryRender);
  }
}

/* 랭킹 시트 (PC: 오른쪽, 모바일: 아래 서랍) */
var sheets = [];
function mountSheet(host, closable) {
  var n = $('tplSheet').content.firstElementChild.cloneNode(true);
  if (!closable) n.querySelector('.x').style.display = 'none';
  else n.querySelector('.x').onclick = function () { $('drawer').classList.remove('on'); };
  n.querySelectorAll('.tabs button').forEach(function (b) { b.textContent = b.dataset.t === 'today' ? t('tabToday') : t('tabAll'); b.onclick = function () { tab = b.dataset.t; renderSheets(); }; });
  host.appendChild(n); sheets.push(n);
}
function renderSheets() {
  sheets.forEach(function (n) {
    n.querySelector('h3 span').textContent = tab === 'today' ? t('sheetToday') : t('sheetAll');
    n.querySelectorAll('.tabs button').forEach(function (b) { b.classList.toggle('on', b.dataset.t === tab); });
    var meEl = n.querySelector('.me');
    if (user) {
      var td = me && me.today;
      meEl.innerHTML = '<div class="nick">' + esc(me ? me.nickname : '…') + (me && me.tier ? ' <em class="tier">' + esc(tierName(me.tier)) + '</em>' : '') + ' <button class="ed">' + t('editNick') + '</button></div>' +
        (td ? t('meToday', { rank: td.rank, score: won(td.score) }) : t('meNone')) + (me ? t('streak', { n: me.streak }) : '');
      meEl.querySelector('.ed').onclick = editNick;
    } else {
      var b = bestToday();
      meEl.innerHTML = (b ? t('meBest', { best: won(b.score) }) : t('meLogin')) + loginButtons('', false);
      bindLogin(meEl);
    }
    var l = board[tab], list = n.querySelector('.list');
    if (l === null) { list.innerHTML = '<div class="empty">' + t('loading') + '</div>'; return; }
    if (l === 'err') { list.innerHTML = '<div class="empty">' + t('loadFail') + '</div>'; return; }
    if (!l.length) { list.innerHTML = '<div class="empty">' + (tab === 'today' ? t('emptyToday') : t('emptyAll')) + '</div>'; return; }
    list.innerHTML = '';
    l.forEach(function (r) {
      var d = document.createElement('div'); d.className = 'it' + (r.is_me ? ' mine' : '');
      d.innerHTML = '<span class="r">' + r.rank + '</span><span class="n">' + esc(r.nickname) + (r.tier ? ' <em class="tier">' + esc(tierName(r.tier)) + '</em>' : '') + '</span><span class="s">' + wonShort(Number(r.score)) + '</span>';
      var ic = document.createElement('canvas'); ic.width = ic.height = 48; iconCanvas(ic, Math.min(10, r.top_level)); d.appendChild(ic);
      list.appendChild(d);
    });
    if (user) { var a = document.createElement('a'); a.className = 'logout'; a.href = '#'; a.textContent = t('logout'); a.onclick = function (e) { e.preventDefault(); logout(); }; list.appendChild(a); }
  });
}
function editNick() {
  var v = prompt(t('nickPrompt'), me ? (me.raw_nickname || me.nickname) : '');
  if (v == null) return;
  rpc('coin_set_nickname', { p_nick: v }).then(function (n) { if (me) me.nickname = n; toast(t('nickSet') + n); loadBoard(); })
    .catch(function () { toast(t('nickErr')); });
}

$('openRank').onclick = function () { $('drawer').classList.add('on'); ga('event', 'mm_rank_open'); loadBoard(); };
$('seeRank').onclick = function () { if (window.innerWidth >= 900) { loadBoard(); return; } $('drawer').classList.add('on'); loadBoard(); };
$('drawer').addEventListener('click', function (e) { if (e.target === this) this.classList.remove('on'); });

/* 공유 */
$('shareBtn').onclick = function () {
  var r = lastResult; if (!r) return;
  var bar = ''; for (var i = 0; i <= r.top; i++) bar += i < 4 ? '🪙' : i < 8 ? '💵' : i === 8 ? '🥇' : i === 9 ? '🏢' : '👑';
  var txt = t('shareText', { n: dayNo(r.day), bar: bar, score: won(r.score), lv: LV[r.top].k, rank: r.rank ? t('shareRank', { rank: r.rank, total: r.total }) : '' });
  var url = 'https://www.apholdings.kr/play/?utm_source=share&utm_medium=social' + (LANG === 'en' ? '&lang=en' : '');
  ga('event', 'mm_share', { rank: r.rank || 0, top_level: r.top });
  if (navigator.share) { navigator.share({ title: t('shareTitle'), text: txt, url: url }).catch(function () {}); return; }
  var full = txt + ' ' + url;
  (navigator.clipboard ? navigator.clipboard.writeText(full) : Promise.reject()).then(function () { toast(t('copied')); })
    .catch(function () { prompt(t('copyPrompt'), full); });
};

$('startBtn').onclick = start;
$('againBtn').onclick = start;
$('mute').onclick = function () { muted = !muted; store.set('mute', muted); setMuteIcon(); };
$('langBtn').onclick = function () { var next = LANG === 'ko' ? 'en' : 'ko'; store.set('lang', next); location.href = location.pathname + '?lang=' + next; };
$('inappOpen').onclick = openInBrowser;
$('inappCopy').onclick = function () { copyUrl('https://www.apholdings.kr/play/' + (LANG === 'en' ? '?lang=en' : '')); };
$('inappKakao').onclick = function () { $('ovInapp').classList.remove('on'); login('kakao'); };
$('inappClose').onclick = function () { $('ovInapp').classList.remove('on'); };

/* 정적 문구 적용 */
(function applyLang() {
  document.documentElement.lang = LANG; document.title = t('title');
  var map = { stTitle: 'stTitle', stSub: 'stSub', how1: 'how1', how2: 'how2', how3: 'how3', stNote: 'stNote', inTitle: 'inTitle', inP: 'inP', inSmall: 'inSmall' };
  for (var id in map) { var el = $(id); if (el) el.innerHTML = t(map[id]); }
  var txt = { startBtn: 'start', againBtn: 'again', shareBtn: 'share', seeRank: 'seeRank', inappOpen: 'inOpen', inappCopy: 'inCopy', inappClose: 'close', openRankLabel: 'rankBtn', footLink: 'footLink', langBtn: 'langBtn' };
  for (var id2 in txt) { var el2 = $(id2); if (el2) el2.textContent = t(txt[id2]); }
  $('inappKakao').innerHTML = KICON + t('inKakao');
  $('hudTitle').textContent = t('shareTitle');
  $('footText').textContent = t('foot');
})();
// 홈페이지 공용 통계 안내문(본문 끝에 붙음)을 하단 한 줄 접이식으로 옮긴다 — 게임 화면을 가리지 않게
(function moveNotice(n) {
  var a = document.querySelector('body > aside[aria-label="방문 통계 안내"]');
  if (!a) { if (n < 20) setTimeout(function () { moveNotice(n + 1); }, 500); return; }
  var d = document.createElement('details'); d.className = 'stat-note';
  var s = document.createElement('summary'); s.textContent = t('statNote'); d.appendChild(s);
  a.removeAttribute('style'); d.appendChild(a); $('foot').appendChild(d);
})(0);

/* ---------- 부팅 ---------- */
window.addEventListener('resize', resize);
if (window.ResizeObserver) new ResizeObserver(resize).observe($('stage'));
mountSheet($('side'), false); mountSheet($('drawer'), true);
setMuteIcon(); buildDex(); resize();
$('dayNo').textContent = t('board') + dayNo(today);
updHud();
R = rng(hashStr('money-merge:' + today)); cur = pickLv(); nxt = pickLv(); drawNext();
engine = Engine.create(); world = engine.world;
var b0 = bestToday(); if (b0) { $('startBtn').textContent = t('startAgain'); }
requestAnimationFrame(loop);

if (sb) {
  sb.auth.getSession().then(function (r) {
    user = r.data && r.data.session ? r.data.session.user : null;
    var pend = store.get('pending', null);
    if (user && (pend || /[?&]code=/.test(location.search))) ga('event', 'mm_login_success', { had_pending: pend ? 1 : 0 });
    if (/[?&](code|utm_source)=/.test(location.search) && history.replaceState) { try { history.replaceState(null, '', location.pathname + (LANG === 'en' ? '?lang=en' : '')); } catch (e) {} }
    if (user && pend) {
      store.set('pending', null);
      if (pend.day === kstDay() || pend.day === kstDay(Date.now() - 864e5)) {
        submit(pend).then(function (x) { toast(t('posted', { rank: x.rank })); if (window.innerWidth < 900) $('drawer').classList.add('on'); return loadMe(); })
          .catch(function () { toast(t('postFail')); }).then(loadBoard);
        return;
      }
    }
    loadMe().then(loadBoard);
  });
  sb.auth.onAuthStateChange(function (ev, session) {
    var u = session ? session.user : null;
    if ((u && u.id) !== (user && user.id)) { user = u; loadMe().then(renderSheets); }
  });
} else { board.today = board.all = 'err'; renderSheets(); }

// 테스트·봇·녹화용 훅 (점수 조작 불가: 서버는 낙하 수·시간으로 검증)
window.__mm = {
  get items() { return items.map(function (b) { return { x: b.position.x, y: b.position.y, lv: b.lv, r: LV[b.lv].r }; }); },
  get state() { return state; }, get score() { return score; }, get cur() { return cur; }, get nxt() { return nxt; },
  get drops() { return drops; }, get top() { return maxLv; }, get log() { return eventLog; }, get lang() { return LANG; },
  get ready() { return performance.now() >= canDropAt; }, radii: LV.map(function (l) { return l.r; }), W: W, H: H, dangerY: DANGER_Y,
  drop: function (x) { aimX = aimTarget = x; canDropAt = 0; drop(); }, aimAt: function (x) { aimTarget = x; }, over: function () { gameOver(); },
  get aim() { return { x: aimX, target: aimTarget, ptr: lastPtr }; }
};
})();

/* 머니 머지 봇 플레이 + 세로 영상 녹화
   node bot.js --url http://localhost:8765/play/?lang=en --out /path/clip --cap "hook text" ...
   결과: <out>.mp4 (1080x1920, 15~20초), <out>.json (점수·단계·낙하·시간·이벤트) */
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execSync } = require('child_process');

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i >= 0 ? process.argv[i + 1] : d; };
const URL = arg('url', 'http://localhost:8765/play/?lang=en');
const OUT = arg('out', '/home/claude/bot/out/clip');
const MAX_DROPS = +arg('maxDrops', 400);
const FULL = arg('full', '0') === '1'; // 1이면 전체 길이 그대로 (편집 없이)

(async () => {
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  const frameDir = OUT + '_frames'; fs.rmSync(frameDir, { recursive: true, force: true }); fs.mkdirSync(frameDir, { recursive: true });
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2, locale: 'en-US', hasTouch: true, isMobile: true });
  const page = await ctx.newPage();
  await page.goto(URL); await page.waitForTimeout(1200);
  const W = await page.evaluate(() => window.__mm.W), H = await page.evaluate(() => window.__mm.H), DANGER = await page.evaluate(() => window.__mm.dangerY);
  const radii = await page.evaluate(() => window.__mm.radii);

  // 캡션 레이어 (영어 단독) — 페이지 안에 그려서 녹화에 그대로 들어가게
  await page.evaluate(() => {
    const s = document.createElement('style');
    s.textContent = `
      .cap{position:fixed;left:16px;right:16px;z-index:50;text-align:center;font-family:"Noto Sans KR",system-ui,sans-serif;pointer-events:none;transition:opacity .25s}
      .cap.top{top:150px}.cap.bot{bottom:120px}
      .cap b{display:inline-block;background:rgba(14,26,43,.85);color:#F5F1E8;font-weight:900;font-size:30px;line-height:1.25;padding:10px 16px;border-radius:14px;box-shadow:0 6px 24px rgba(0,0,0,.35)}
      .cap b.gold{background:#F5C542;color:#2A1C00}
      .cap small{display:block;margin-top:8px;font-size:15px;font-weight:700;color:#F5F1E8;text-shadow:0 1px 4px rgba(0,0,0,.6)}
      .badge{position:fixed;left:50%;transform:translateX(-50%);top:104px;white-space:nowrap;z-index:50;background:rgba(245,197,66,.95);color:#2A1C00;font:900 13px/1 "Noto Sans KR",sans-serif;padding:8px 12px;border-radius:99px;letter-spacing:.04em;pointer-events:none}
      .endcard{position:fixed;inset:0;z-index:60;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(9,16,28,.78);backdrop-filter:blur(4px);color:#F5F1E8;font-family:"Noto Sans KR",system-ui,sans-serif;text-align:center;padding:24px}
      .endcard .n{font-size:16px;font-weight:700;color:#93A3B8;letter-spacing:.08em}
      .endcard .s{font-size:56px;font-weight:900;color:#F5C542;margin:6px 0 2px;letter-spacing:-.02em}
      .endcard .m{font-size:17px;font-weight:700}
      .endcard .q{margin-top:26px;font-size:30px;font-weight:900;line-height:1.2}
      .endcard .c{margin-top:14px;background:#F5C542;color:#2A1C00;font-weight:900;font-size:18px;padding:12px 20px;border-radius:99px}
      .endcard .u{margin-top:10px;font-size:13px;color:#93A3B8;font-weight:700}
      #toast,.stat-note{display:none!important}`;
    document.head.appendChild(s);
    window.__cap = (where, html, gold) => { let el = document.getElementById('cap_' + where); if (!el) { el = document.createElement('div'); el.id = 'cap_' + where; el.className = 'cap ' + where; document.body.appendChild(el); } el.innerHTML = html ? `<b class="${gold ? 'gold' : ''}">${html}</b>` : ''; el.style.opacity = html ? 1 : 0; };
    window.__badge = (txt) => { let el = document.getElementById('badge'); if (!el) { el = document.createElement('div'); el.id = 'badge'; el.className = 'badge'; document.body.appendChild(el); } el.textContent = txt || ''; el.style.display = txt ? '' : 'none'; };
    window.__end = (html) => { let el = document.getElementById('endcard'); if (!el) { el = document.createElement('div'); el.id = 'endcard'; el.className = 'endcard'; document.body.appendChild(el); } el.innerHTML = html; };
  });

  // 녹화 시작 (1080x1920, 약 30fps)
  const cdp = await ctx.newCDPSession(page);
  const frames = []; let fi = 0; const t0 = Date.now();
  cdp.on('Page.screencastFrame', async (ev) => {
    const f = path.join(frameDir, String(fi++).padStart(6, '0') + '.jpg');
    fs.writeFileSync(f, Buffer.from(ev.data, 'base64'));
    frames.push({ f, t: ev.metadata.timestamp * 1000 });
    try { await cdp.send('Page.screencastFrameAck', { sessionId: ev.sessionId }); } catch (e) {}
  });
  await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 85, maxWidth: 1080, maxHeight: 1920, everyNthFrame: 2 });
  const now = () => Date.now() - t0;
  const marks = {};

  await page.evaluate(() => window.__cap('top', 'Can you beat an AI<br>at making money?'));
  await page.waitForTimeout(1600);
  await page.click('#startBtn');
  marks.start = now();
  await page.evaluate(() => { window.__cap('top', '₩10 coins → merge → a building'); window.__badge('LIA (AI) IS PLAYING'); });
  setTimeout(() => page.evaluate(() => window.__cap('top', '')).catch(() => {}), 2600);

  // ---- 봇 정책 ----
  const landing = (items, x, rc) => {
    let y = H - rc - 3, hit = null;
    for (const it of items) { const dx = Math.abs(x - it.x), rr = it.r + rc; if (dx < rr) { const yy = it.y - Math.sqrt(rr * rr - dx * dx); if (yy < y) { y = yy; hit = it; } } }
    return { y, hit };
  };
  const choose = (items, cur) => {
    const rc = radii[cur]; let best = null;
    for (let x = rc + 2; x <= W - rc - 2; x += 5) {
      const { y, hit } = landing(items, x, rc);
      let sc = y; // 깊을수록 좋음
      const near = items.filter(it => Math.hypot(it.x - x, it.y - y) <= it.r + rc + 2);
      const same = near.filter(it => it.lv === cur);
      if (same.length) sc += 900 + cur * 120 + (same.length - 1) * 200;        // 같은 돈 옆에 떨어뜨리기
      const bigger = near.filter(it => it.lv === cur + 1);
      if (bigger.length) sc += 60;                                             // 다음 단계 옆이면 소폭 가점
      if (y - rc < DANGER + 70) sc -= 700;                                    // 위험선 근처는 회피
      if (hit && hit.lv < cur && hit.lv <= 2) sc -= 120 * (cur - hit.lv);     // 큰 돈을 작은 돈 위에 올리지 않기
      if (!hit) sc += 40;                                                      // 바닥이면 가점
      if (best === null || sc > best.sc) best = { x, sc, y };
    }
    return best;
  };
  const settled = async () => {
    for (let i = 0; i < 8; i++) {
      const a = await page.evaluate(() => window.__mm.items); await page.waitForTimeout(110);
      const b = await page.evaluate(() => window.__mm.items);
      if (a.length !== b.length) continue;
      let mx = 0; for (let k = 0; k < a.length; k++) mx = Math.max(mx, Math.hypot(a[k].x - b[k].x, a[k].y - b[k].y));
      if (mx < 0.6) return;
    }
  };

  let drops = 0, lastScore = 0, bigMergeAt = null, bigMergeLv = 0;
  while (drops < MAX_DROPS) {
    const st = await page.evaluate(() => ({ state: window.__mm.state, cur: window.__mm.cur, items: window.__mm.items, score: window.__mm.score, top: window.__mm.top, ready: window.__mm.ready }));
    if (st.state !== 'play') break;
    if (!st.ready) { await page.waitForTimeout(60); continue; }
    await settled();
    const st2 = await page.evaluate(() => ({ state: window.__mm.state, cur: window.__mm.cur, items: window.__mm.items }));
    if (st2.state !== 'play') break;
    const pick = choose(st2.items, st2.cur);
    await page.evaluate((x) => window.__mm.aimAt(x), pick.x);
    await page.waitForTimeout(170);
    await page.evaluate((x) => window.__mm.drop(x), pick.x);
    drops++;
    const sc = await page.evaluate(() => ({ s: window.__mm.score, top: window.__mm.top }));
    if (sc.top >= 6 && sc.top > bigMergeLv) { bigMergeLv = sc.top; bigMergeAt = now(); }
    lastScore = sc.s;
    await page.waitForTimeout(260);
  }
  // 종료 대기
  for (let i = 0; i < 60; i++) { if ((await page.evaluate(() => window.__mm.state)) === 'over') break; await page.waitForTimeout(250); }
  marks.over = now();
  await page.waitForTimeout(900);
  const res = await page.evaluate(() => ({ score: window.__mm.score, top: window.__mm.top, drops: window.__mm.drops, log: window.__mm.log, lang: window.__mm.lang, day: document.getElementById('dayNo').textContent }));
  const won = (n) => n >= 1e9 ? '₩' + (n / 1e9).toFixed(1) + 'B' : n >= 1e6 ? '₩' + (n / 1e6).toFixed(1) + 'M' : '₩' + n.toLocaleString('en-US');
  const lvName = ['₩10', '₩50', '₩100', '₩500', '₩1,000', '₩5,000', '₩10,000', '₩50,000', 'Gold bar', 'Building', 'AP'][res.top];
  const boardNo = (res.day.match(/\d+/) || ['?'])[0];
  // 끝 카드
  await page.evaluate(({ score, lvName, boardNo }) => {
    document.querySelectorAll('.ov').forEach(o => o.classList.remove('on'));
    window.__badge(''); window.__cap('top', '');
    window.__end(`<div class="n">LIA (AI) · BOARD #${boardNo} · AI SCORE</div><div class="s">${score}</div><div class="m">reached ${lvName}</div><div class="q">Beat me and your name<br>goes above mine.</div><div class="c">Comment BEAT 👇</div><div class="u">apholdings.kr/play · same board for everyone today</div>`);
  }, { score: won(res.score), lvName, boardNo });
  marks.end = now();
  await page.waitForTimeout(3200);
  marks.stop = now();
  await cdp.send('Page.stopScreencast');
  await browser.close();

  // ---- 편집: 처음 4초 1배 → 중간 빨리감기 → 마지막 7초 1배 → 끝 카드 3초 ----
  const base = frames[0].t;
  const srcAt = (ms) => { let lo = 0, hi = frames.length - 1; while (lo < hi) { const mid = (lo + hi + 1) >> 1; if (frames[mid].t - base <= ms) lo = mid; else hi = mid - 1; } return frames[lo].f; };
  const fps = 30, list = [];
  const push = (srcMs) => list.push(srcAt(srcMs));
  const total = frames[frames.length - 1].t - base;
  if (FULL) { for (let ms = 0; ms < total; ms += 1000 / fps) push(ms); }
  else {
    const seg1End = Math.min(marks.start + 3000, marks.over), tailStart = Math.max(seg1End, marks.over - 7000);
    for (let ms = 0; ms < seg1End; ms += 1000 / fps) push(ms);
    const midLen = tailStart - seg1End, target = Math.min(8000, midLen), speed = midLen > 0 ? midLen / Math.max(target, 1) : 1;
    for (let o = 0; o < target; o += 1000 / fps) push(seg1End + o * speed);
    for (let ms = tailStart; ms < marks.stop; ms += 1000 / fps) push(ms);
  }
  const listFile = OUT + '_list.txt';
  fs.writeFileSync(listFile, list.map(f => `file '${f}'\nduration ${(1 / fps).toFixed(5)}`).join('\n') + `\nfile '${list[list.length - 1]}'\n`);
  execSync(`ffmpeg -y -loglevel error -f concat -safe 0 -i "${listFile}" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=#0E1A2B,format=yuv420p" -r ${fps} -c:v libx264 -preset veryfast -crf 20 -movflags +faststart "${OUT}.mp4"`);
  fs.writeFileSync(OUT + '.json', JSON.stringify({ ...res, marks, seconds: list.length / fps, frames: frames.length, url: URL, recordedAt: new Date().toISOString() }, null, 1));
  fs.rmSync(frameDir, { recursive: true, force: true }); fs.rmSync(listFile, { force: true });
  console.log(JSON.stringify({ score: res.score, top: res.top, drops: res.drops, seconds: list.length / fps, out: OUT + '.mp4' }));
})().catch(e => { console.error(e); process.exit(1); });

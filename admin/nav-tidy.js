// 사이드바 메뉴 정리 — 안 쓰는 메뉴를 숨긴다. (2026-10-02 대표 지시 「숨기기 기능도 넣어」)
//
// 「메뉴 정리」를 누르면 메뉴마다 눈 표시가 붙고, 누르는 대로 숨김/보임이 바뀐다. 다 됐으면 「완료」.
// 숨긴 메뉴는 이 브라우저에만 기억한다(사람마다 쓰는 메뉴가 다르다). 지워지거나 막혀 있으면 전부 보인다 —
// 숨긴 걸 다시 못 찾게 되는 쪽보다 다 보이는 쪽이 낫다.
// Overview 는 숨길 수 없다 — 다 숨기면 돌아올 곳이 없다.
const KEY = 'admin.navHidden';
const LOCKED = new Set(['overview']);

function readHidden() {
  try { return new Set(JSON.parse(localStorage.getItem(KEY) || '[]')); } catch { return new Set(); }
}
function writeHidden(set) {
  try { localStorage.setItem(KEY, JSON.stringify([...set])); } catch { /* 사생활 보호 모드 — 이번 창에서만 */ }
}

export function initNavTidy() {
  const nav = document.querySelector('.sidebar nav');
  if (!nav) return;
  let hidden = readHidden();
  let editing = false;

  const toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = 'nav-tidy';
  nav.after(toggle);

  // 메뉴 하나 = data-section 을 가진 버튼. 묶음(앱 현황)의 부모를 숨기면 묶음째 숨는다.
  const items = () => [...nav.querySelectorAll('.nav-item[data-section]')];

  function paint() {
    document.body.classList.toggle('nav-editing', editing);
    items().forEach((b) => {
      const key = b.dataset.section;
      const off = hidden.has(key);
      const target = b.classList.contains('nav-parent') ? b.closest('.nav-group') : b;
      target.classList.toggle('nav-off', off);
      b.classList.toggle('nav-off-self', off);
      if (LOCKED.has(key)) b.dataset.locked = '1';
      b.setAttribute('aria-pressed', editing ? String(!off) : 'false');
    });
    const n = hidden.size;
    toggle.textContent = editing ? '완료' : (n ? `메뉴 정리 · ${n}개 숨김` : '메뉴 정리');
    toggle.setAttribute('aria-pressed', String(editing));
  }

  toggle.addEventListener('click', () => { editing = !editing; paint(); });

  // 편집 중에는 메뉴를 눌러도 화면을 바꾸지 않고 숨김/보임만 바꾼다.
  // 캡처 단계에서 먼저 받아 문서 쪽 클릭 처리(화면 전환)까지 가지 않게 막는다.
  nav.addEventListener('click', (event) => {
    if (!editing) return;
    const b = event.target.closest('.nav-item[data-section]');
    if (!b) return;
    event.preventDefault();
    event.stopPropagation();
    const key = b.dataset.section;
    if (LOCKED.has(key)) return;
    if (hidden.has(key)) hidden.delete(key); else hidden.add(key);
    writeHidden(hidden);
    paint();
  }, true);

  paint();
}

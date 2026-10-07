(() => {
  const hero = document.querySelector('[data-lia-hero]');
  if (!hero) return;
  const stage = hero.querySelector('[data-lia-stage]');
  const toggle = hero.querySelector('[data-lia-toggle]');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  let enabled = !reduced.matches;
  let greeting = false;
  let frame = 0;
  let point;
  let hoveringLink = false;
  let focusedLink = false;
  const neutral = () => {
    stage.dataset.pose = 'neutral';
    stage.style.removeProperty('--lia-rx');
    stage.style.removeProperty('--lia-ry');
    stage.setAttribute('aria-pressed', 'false');
  };
  const hello = () => {
    stage.dataset.pose = 'hello';
    stage.style.removeProperty('--lia-rx');
    stage.style.removeProperty('--lia-ry');
    stage.setAttribute('aria-pressed', 'true');
  };
  const syncToggle = () => {
    toggle.setAttribute('aria-pressed', String(enabled));
    toggle.textContent = enabled ? toggle.dataset.on : toggle.dataset.off;
  };
  hero.addEventListener('pointermove', event => {
    if (!enabled || reduced.matches || event.pointerType !== 'mouse' || greeting || hoveringLink || focusedLink) return;
    point = {x: event.clientX, y: event.clientY};
    if (frame) return;
    frame = requestAnimationFrame(() => {
      frame = 0;
      if (!enabled || greeting || hoveringLink || focusedLink) return;
      const box = stage.getBoundingClientRect();
      const x = Math.max(-1, Math.min(1, (point.x - box.left - box.width / 2) / (box.width / 2)));
      const y = Math.max(-1, Math.min(1, (point.y - box.top - box.height / 2) / (box.height / 2)));
      stage.dataset.pose = Math.abs(x) > .35 && Math.abs(x) >= Math.abs(y) ? (x < 0 ? 'left' : 'right') : Math.abs(y) > .4 ? (y < 0 ? 'up' : 'down') : 'neutral';
      stage.style.setProperty('--lia-rx', `${-y * 2}deg`);
      stage.style.setProperty('--lia-ry', `${x * 3}deg`);
    });
  });
  hero.addEventListener('pointerleave', () => { if (!greeting && !focusedLink) neutral(); });
  stage.addEventListener('click', () => { if (!enabled) return; greeting = !greeting; greeting ? hello() : neutral(); });
  toggle.addEventListener('click', () => { enabled = !enabled; greeting = false; neutral(); syncToggle(); });
  reduced.addEventListener('change', () => { enabled = !reduced.matches; greeting = false; neutral(); syncToggle(); });
  hero.querySelectorAll('[data-lia-greet]').forEach(link => {
    link.addEventListener('pointerenter', () => { hoveringLink = true; if (enabled) hello(); });
    link.addEventListener('pointerleave', () => { hoveringLink = false; if (!greeting && !focusedLink) neutral(); });
    link.addEventListener('focus', () => { focusedLink = true; if (enabled) hello(); });
    link.addEventListener('blur', () => { focusedLink = false; if (!greeting && !hoveringLink) neutral(); });
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && frame) { cancelAnimationFrame(frame); frame = 0; }
  });
  syncToggle();
})();

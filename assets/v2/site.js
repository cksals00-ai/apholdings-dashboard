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
const film = document.getElementById('brand-motion');
if (film) {
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
}

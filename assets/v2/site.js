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

/* Local prototype interactions. No credentials or selected files are sent anywhere. */
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

// Keep the original Figma proportions visible at any browser window size.
function fitScreensToWindow() {
  const frames = $('.frames');
  if (frames) {
    const previews = $$('.frame-preview', frames);
    const gap = parseFloat(getComputedStyle(frames).gap) || 0;
    const captionHeight = Math.max(...previews.map(preview => {
      const caption = $('figcaption', preview);
      return caption.offsetHeight + parseFloat(getComputedStyle(caption).marginBottom);
    }));
    const scale = Math.max(0, Math.min(1,
      (frames.clientWidth - gap * (previews.length - 1)) / (402 * previews.length),
      (frames.clientHeight - captionHeight) / 992));
    frames.style.setProperty('--preview-width', `${402 * scale}px`);
    frames.style.setProperty('--preview-height', `${992 * scale}px`);
  }
  const phone = $('.phone');
  if (phone) {
    const scale = Math.min(1, window.innerWidth / 402, window.innerHeight / 992);
    phone.style.setProperty('--screen-scale', scale);
  }
}
fitScreensToWindow();
window.addEventListener('resize', fitScreensToWindow);
document.fonts.ready.then(fitScreensToWindow);

$('#signin-form')?.addEventListener('submit', event => {
  event.preventDefault();
  window.location.href = 'dashboard.html';
});
$('.show-password')?.addEventListener('click', event => {
  const input = $('#password');
  const visible = input.type === 'password';
  input.type = visible ? 'text' : 'password';
  event.currentTarget.setAttribute('aria-pressed', String(visible));
  event.currentTarget.setAttribute('aria-label', visible ? 'Hide password' : 'Show password');
});

const info = {
  recovery: ['Reset your password', 'Contact your university administrator to reset your student portal password.'],
  admin: ['Contact Admin', 'Your university administrator can help create your student account.'],
  calendar: ['Academic calendar', 'Fall 2026 · Week 7. Problem Set 04 is due October 16. Spring course registration opens October 26.'],
  course: ['Data Structures', 'CS204 · Room B-204. This prototype includes the Data Structures academic details.']
};
$$('[data-info]').forEach(button => button.addEventListener('click', () => {
  const [title, message] = info[button.dataset.info];
  $('#info-title').textContent = title;
  $('#info-message').textContent = message;
  $('#info-dialog').showModal();
}));
$$('[data-dialog]').forEach(button => button.addEventListener('click', () => {
  document.getElementById(button.dataset.dialog).showModal();
}));
$$('[data-close]').forEach(button => button.addEventListener('click', () => button.closest('dialog').close()));
$('#assignment-form')?.addEventListener('submit', event => {
  event.preventDefault();
  window.location.href = 'submission.html';
});

let activeFilter = 'all';
function applyNotificationFilter() {
  const prefs = $('#preferences-form');
  $$('.notification').forEach(card => {
    const preference = prefs?.elements.namedItem(card.dataset.category);
    const enabled = !preference || preference.checked;
    const matches = activeFilter === 'all' || (activeFilter === 'unread' && card.dataset.unread === 'true') ||
      (activeFilter === 'deadlines' && (card.classList.contains('compact') || card.dataset.category === 'registration'));
    card.hidden = !enabled || !matches;
  });
  $$('.notification-group').forEach(group => group.hidden = !$('.notification:not([hidden])', group));
  const empty = $('.empty-notifications');
  if (empty) empty.hidden = Boolean($('.notification:not([hidden])'));
}
$$('[data-filter]').forEach(button => button.addEventListener('click', () => {
  activeFilter = button.dataset.filter;
  $$('[data-filter]').forEach(item => {
    item.classList.toggle('active', item === button);
    item.setAttribute('aria-pressed', String(item === button));
  });
  applyNotificationFilter();
}));
$('#mark-read')?.addEventListener('click', () => {
  $$('.notification').forEach(card => { card.dataset.unread = 'false'; card.classList.remove('unread'); });
  $$('.unread-dot').forEach(dot => dot.hidden = true);
  $('#unread-count').textContent = '0';
  applyNotificationFilter();
});
$('#preferences-form')?.addEventListener('submit', event => {
  event.preventDefault();
  applyNotificationFilter();
  $('#preferences-dialog').close();
});

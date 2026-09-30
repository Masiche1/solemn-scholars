// Tutorly — front-end interactions
document.addEventListener('DOMContentLoaded', function () {
  // Mobile nav toggle
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      nav.classList.toggle('open');
    });
  }

  // Auto-dismiss flash messages
  document.querySelectorAll('.alert').forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity .4s';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 400);
    }, 5000);
  });

  // Availability day toggles in tutor profile editor
  document.querySelectorAll('[data-avail-toggle]').forEach(function (cb) {
    cb.addEventListener('change', function () {
      const wrap = cb.closest('.avail-day-row');
      if (wrap) {
        wrap.querySelectorAll('input[type="time"]').forEach(function (t) {
          t.disabled = !cb.checked;
        });
      }
    });
  });

  // Live tutor search (homepage hero quick search) -> redirect to directory
  const quickSearch = document.querySelector('[data-quick-search]');
  if (quickSearch) {
    quickSearch.addEventListener('submit', function (e) {
      // default form submit is fine; no JS needed
    });
  }
});

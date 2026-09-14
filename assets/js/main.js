/* With Nadine — site behaviour
   Language switch (EN / العربية), mobile nav, accordions, scroll reveal, forms. */
(function () {
  'use strict';

  var root = document.documentElement;
  var STORE_KEY = 'wn-lang';

  /* ---------------------------------------------------------------- language */
  function readStored() {
    try { return localStorage.getItem(STORE_KEY); } catch (e) { return null; }
  }
  function writeStored(v) {
    try { localStorage.setItem(STORE_KEY, v); } catch (e) { /* private mode */ }
  }

  function setLang(lang) {
    var ar = lang === 'ar';
    root.setAttribute('lang', ar ? 'ar' : 'en');
    root.setAttribute('dir', ar ? 'rtl' : 'ltr');
    document.querySelectorAll('[data-set-lang]').forEach(function (btn) {
      btn.setAttribute('aria-pressed', String(btn.getAttribute('data-set-lang') === lang));
    });
    writeStored(lang);
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-set-lang]');
    if (!btn) return;
    setLang(btn.getAttribute('data-set-lang'));
  });

  setLang(readStored() === 'ar' ? 'ar' : 'en');

  /* -------------------------------------------------------------- mobile nav */
  var burger = document.querySelector('.burger');
  var links = document.getElementById('nav-links');
  var header = document.querySelector('.site-header');

  function syncHeaderHeight() {
    if (header) root.style.setProperty('--header-h', header.offsetHeight + 'px');
  }
  syncHeaderHeight();
  window.addEventListener('resize', syncHeaderHeight);

  if (burger && links) {
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      links.classList.toggle('is-open', !open);
    });
    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        burger.setAttribute('aria-expanded', 'false');
        links.classList.remove('is-open');
      }
    });
    window.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && links.classList.contains('is-open')) {
        burger.setAttribute('aria-expanded', 'false');
        links.classList.remove('is-open');
        burger.focus();
      }
    });
  }

  /* ------------------------------------------------------------ sticky shade */
  if (header) {
    var onScroll = function () { header.classList.toggle('is-stuck', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* -------------------------------------------------------------- accordions */
  document.addEventListener('click', function (e) {
    var trigger = e.target.closest('[data-accordion]');
    if (!trigger) return;
    var panel = document.getElementById(trigger.getAttribute('aria-controls'));
    if (!panel) return;
    var open = trigger.getAttribute('aria-expanded') === 'true';
    trigger.setAttribute('aria-expanded', String(!open));
    panel.classList.toggle('is-open', !open);
  });

  /* ----------------------------------------------------------- scroll reveal */
  var reveals = document.querySelectorAll('.reveal');
  if (reveals.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ------------------------------------------------------------------- forms
     No endpoint is wired up yet. Set data-endpoint on the <form> to your email
     provider's POST URL (Kit / Mailchimp / Formspree) and submissions will go
     there. Until then the form says so plainly instead of pretending to send. */
  document.querySelectorAll('form[data-wn-form]').forEach(function (form) {
    var msg = form.querySelector('.form__msg');
    form.addEventListener('submit', function (e) {
      var endpoint = form.getAttribute('data-endpoint');
      if (endpoint) return; // let the browser post it for real
      e.preventDefault();
      if (!msg) return;
      msg.hidden = false;
      msg.innerHTML =
        '<span data-lang="en">This form isn\'t connected to an email service yet. ' +
        'Add your provider\'s URL to <code>data-endpoint</code> on this form, or email ' +
        '<a href="mailto:hello@withnadine.com">hello@withnadine.com</a> in the meantime.</span>' +
        '<span data-lang="ar">هذا النموذج غير موصول بخدمة بريد إلكتروني بعد. ' +
        'أضيفي رابط مزوّد الخدمة في <code>data-endpoint</code>، أو راسلينا على ' +
        '<a href="mailto:hello@withnadine.com">hello@withnadine.com</a> مؤقتاً.</span>';
      msg.focus && msg.focus();
    });
  });

  /* ------------------------------------------------------------------- year */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();

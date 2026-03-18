/**
 * Monad System — Runtime
 * Generated from the Monad System build. Do not edit directly.
 *
 * Handles:
 *   Akasha  — theme toggle ([data-mn-theme-toggle]), persists to localStorage
 *   Threshold — hamburger (.threshold-toggle) + rail drawer (.monad-rail)
 *
 * No dependencies. Drop in <script src="monad.js"></script> before </body>.
 */
(function () {
  'use strict';

  // -----------------------------------------------------------------------
  // Akasha — theme toggle
  // data-akasha="light|dark" on <html>, persists via localStorage
  // Respects prefers-color-scheme as OS fallback.
  // -----------------------------------------------------------------------
  function initAkasha() {
    var root = document.documentElement;
    var stored = localStorage.getItem('mn-akasha');
    if (stored) {
      root.dataset.akasha = stored;
    } else if (window.matchMedia('(prefers-color-scheme: light)').matches) {
      root.dataset.akasha = 'light';
    }
    document.querySelectorAll('[data-mn-theme-toggle]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var next = root.dataset.akasha === 'light' ? 'dark' : 'light';
        root.dataset.akasha = next;
        localStorage.setItem('mn-akasha', next);
      });
    });
  }

  // -----------------------------------------------------------------------
  // Threshold — hamburger nav
  // Toggles .threshold-nav.is-open
  // -----------------------------------------------------------------------
  function initThresholdNav() {
    var btn = document.querySelector('.threshold-toggle');
    var nav = document.querySelector('.threshold-nav');
    if (!btn || !nav) return;

    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', 'mn-threshold-nav');
    nav.id = 'mn-threshold-nav';

    btn.addEventListener('click', function () {
      var isOpen = nav.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(isOpen));
    });

    document.addEventListener('click', function (e) {
      if (!btn.contains(e.target) && !nav.contains(e.target)) {
        nav.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        nav.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // -----------------------------------------------------------------------
  // Threshold — rail drawer (off-canvas sidenav)
  // Toggles .monad-rail.is-open + .threshold-overlay.is-visible
  // Trigger: any [data-mn-rail-toggle]
  // -----------------------------------------------------------------------
  function initRail() {
    var rail = document.querySelector('.monad-rail');
    if (!rail) return;

    var overlay = document.querySelector('.threshold-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.className = 'threshold-overlay';
      overlay.setAttribute('aria-hidden', 'true');
      document.body.appendChild(overlay);
    }

    function openRail() {
      rail.classList.add('is-open');
      overlay.classList.add('is-visible');
      document.body.style.overflow = 'hidden';
      rail.setAttribute('aria-hidden', 'false');
    }

    function closeRail() {
      rail.classList.remove('is-open');
      overlay.classList.remove('is-visible');
      document.body.style.overflow = '';
      rail.setAttribute('aria-hidden', 'true');
    }

    document.querySelectorAll('[data-mn-rail-toggle]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        rail.classList.contains('is-open') ? closeRail() : openRail();
      });
    });

    overlay.addEventListener('click', closeRail);

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeRail();
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 1056) closeRail();
    });
  }

  // -----------------------------------------------------------------------
  // Init
  // -----------------------------------------------------------------------
  function init() {
    initAkasha();
    initThresholdNav();
    initRail();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

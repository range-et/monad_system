/**
 * Design System — Interactive Behaviour
 * Generated from the design system build. Do not edit directly.
 *
 * Handles: theme toggle, hamburger nav, sidenav drawer, overlay backdrop.
 * No dependencies. Drop in <script src="design-system.js"></script> before </body>.
 */
(function () {
  'use strict';

  // -----------------------------------------------------------------------
  // Theme toggle — persists to localStorage, respects prefers-color-scheme
  // -----------------------------------------------------------------------
  function initTheme() {
    var root = document.documentElement;
    var stored = localStorage.getItem('ds-theme');
    if (stored) {
      root.dataset.theme = stored;
    } else if (window.matchMedia('(prefers-color-scheme: light)').matches) {
      root.dataset.theme = 'light';
    }
    document.querySelectorAll('[data-ds-theme-toggle]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var next = root.dataset.theme === 'light' ? 'dark' : 'light';
        root.dataset.theme = next;
        localStorage.setItem('ds-theme', next);
      });
    });
    // Legacy id-based toggle support
    var legacyBtn = document.getElementById('theme-toggle');
    if (legacyBtn && !legacyBtn.dataset.dsThemeToggle) {
      legacyBtn.addEventListener('click', function () {
        var next = root.dataset.theme === 'light' ? 'dark' : 'light';
        root.dataset.theme = next;
        localStorage.setItem('ds-theme', next);
      });
    }
  }

  // -----------------------------------------------------------------------
  // Hamburger nav — toggles .ds-header__nav.is-open
  // -----------------------------------------------------------------------
  function initHamburger() {
    var btn = document.querySelector('.ds-hamburger');
    var nav = document.querySelector('.ds-header__nav');
    if (!btn || !nav) return;

    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', 'ds-header-nav');
    nav.id = 'ds-header-nav';

    btn.addEventListener('click', function () {
      var isOpen = nav.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(isOpen));
    });

    // Close on outside click
    document.addEventListener('click', function (e) {
      if (!btn.contains(e.target) && !nav.contains(e.target)) {
        nav.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });

    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        nav.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // -----------------------------------------------------------------------
  // Sidenav drawer — toggles .ds-sidenav.is-open + overlay
  // Injects an overlay element if not already in DOM.
  // Open trigger: any [data-ds-nav-toggle] or #nav-toggle element.
  // -----------------------------------------------------------------------
  function initSidenav() {
    var sidenav = document.querySelector('.ds-sidenav');
    if (!sidenav) return;

    // Ensure overlay exists
    var overlay = document.querySelector('.ds-nav-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.className = 'ds-nav-overlay';
      overlay.setAttribute('aria-hidden', 'true');
      document.body.appendChild(overlay);
    }

    function openNav() {
      sidenav.classList.add('is-open');
      overlay.classList.add('is-visible');
      document.body.style.overflow = 'hidden';
      sidenav.setAttribute('aria-hidden', 'false');
    }

    function closeNav() {
      sidenav.classList.remove('is-open');
      overlay.classList.remove('is-visible');
      document.body.style.overflow = '';
      sidenav.setAttribute('aria-hidden', 'true');
    }

    // Wire up any toggle triggers
    document.querySelectorAll('[data-ds-nav-toggle]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        sidenav.classList.contains('is-open') ? closeNav() : openNav();
      });
    });

    // Legacy id-based trigger
    var legacyToggle = document.getElementById('nav-toggle');
    if (legacyToggle) {
      legacyToggle.addEventListener('click', function () {
        sidenav.classList.contains('is-open') ? closeNav() : openNav();
      });
    }

    // Close on overlay click
    overlay.addEventListener('click', closeNav);

    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeNav();
    });

    // On resize: close drawer and restore scroll when viewport widens past breakpoint
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1056) {
        closeNav();
      }
    });
  }

  // -----------------------------------------------------------------------
  // Init all on DOM ready
  // -----------------------------------------------------------------------
  function init() {
    initTheme();
    initHamburger();
    initSidenav();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

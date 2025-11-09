/* main.js - initialization and small UI helpers
   This file should be loaded last (after helpers).
*/

(function () {
  "use strict";

  function initNavHighlight() {
    try {
      const path = window.location.pathname;
      document.querySelectorAll('.nav-link, .sidebar-menu a').forEach(link => {
        const href = link.getAttribute('href');
        if (!href) return;
        try {
          if (path === href || (href !== '/' && path.startsWith(href))) {
            link.classList.add('active');
          }
        } catch (e) {}
      });
    } catch (e) {}
  }

  // load HTML includes for static preview (optional - will fail when server-side includes are used)
  function loadIncludes() {
    // Only run when page is served as static files; if using Flask server-side includes, skip
    const canFetch = typeof fetch === 'function' && window.location.protocol.startsWith('http');
    if (!canFetch) return;
    const includeTargets = document.querySelectorAll('[data-include-path]');
    includeTargets.forEach(async (el) => {
      const path = el.getAttribute('data-include-path');
      if (!path) return;
      try {
        const res = await fetch(path);
        if (res.ok) {
          el.innerHTML = await res.text();
        }
      } catch (e) {
        // ignore
      }
    });
  }

  // simple form demo prevention (for static preview)
  function preventEmptyFormSubmits() {
    document.querySelectorAll('form').forEach(form => {
      form.addEventListener('submit', (e) => {
        // if action is '#' or empty, prevent actual navigation
        const action = form.getAttribute('action') || '#';
        if (action === '#' || action.trim() === '') {
          e.preventDefault();
          toast('Form submission intercepted (static preview).', 'info', 2000);
        }
      });
    });
  }

  // run on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', () => {
    initNavHighlight();
    loadIncludes();
    preventEmptyFormSubmits();
    // attach a simple global error handler for development
    window.addEventListener('error', function (evt) {
      console.error('JS Error:', evt.message, 'at', evt.filename + ':' + evt.lineno);
    });
  });

  // expose small helpers (if needed)
  window.initNavHighlight = initNavHighlight;
  window.loadIncludes = loadIncludes;
})();

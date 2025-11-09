/* utils.js - small helpers (attach to window) */

(function () {
  "use strict";

  function formatCurrency(v) {
    try {
      return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(Number(v || 0));
    } catch (e) {
      return '₹' + Number(v || 0).toFixed(2);
    }
  }

  function daysBetween(a, b) {
    try {
      const da = new Date(a);
      const db = new Date(b);
      return Math.round((db - da) / (1000 * 60 * 60 * 24));
    } catch (e) {
      return 0;
    }
  }

  function uid(prefix = 'ID') {
    return prefix + '-' + Math.random().toString(36).slice(2, 9).toUpperCase();
  }

  function isoToday() {
    return new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  }

  // safe DOM helper
  function qs(selector, root = document) {
    return root.querySelector(selector);
  }
  function qsa(selector, root = document) {
    return Array.from(root.querySelectorAll(selector));
  }

  // expose to global
  window.formatCurrency = formatCurrency;
  window.daysBetween = daysBetween;
  window.uid = uid;
  window.isoToday = isoToday;
  window.qs = qs;
  window.qsa = qsa;
})();

/* charts.js - Chart.js helpers (attach to window)
   Assumes Chart.js is loaded globally (via CDN in base.html).
*/

(function () {
  "use strict";

  function safeGetCtx(selectorOrElement) {
    let el = typeof selectorOrElement === 'string' ? document.querySelector(selectorOrElement) : selectorOrElement;
    if (!el) return null;
    if (el.tagName.toLowerCase() === 'canvas') return el.getContext('2d');
    // if a container is provided, try to find canvas inside
    const canvas = el.querySelector('canvas');
    return canvas ? canvas.getContext('2d') : null;
  }

  function renderPieChart(canvasSelector, labels = [], values = [], options = {}) {
    const ctx = safeGetCtx(canvasSelector);
    if (!ctx || typeof Chart === 'undefined') return null;
    return new Chart(ctx, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          data: values,
          backgroundColor: options.colors || ['#007bff','#28a745','#ffc107','#dc3545','#6c757d'],
          borderWidth: 0
        }]
      },
      options: Object.assign({
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom' }
        }
      }, options)
    });
  }

  function renderBarChart(canvasSelector, labels = [], values = [], options = {}) {
    const ctx = safeGetCtx(canvasSelector);
    if (!ctx || typeof Chart === 'undefined') return null;
    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: options.label || 'Amount',
          data: values,
          backgroundColor: options.backgroundColor || '#007bff'
        }]
      },
      options: Object.assign({
        responsive: true,
        maintainAspectRatio: false,
        scales: { y: { beginAtZero: true } },
        plugins: { legend: { display: false } }
      }, options)
    });
  }

  // simple stub to render a small placeholder sparkline (non-Chart.js)
  function renderSparkline(elSelector, values = []) {
    const el = typeof elSelector === 'string' ? document.querySelector(elSelector) : elSelector;
    if (!el) return;
    el.innerHTML = '<div style="height:40px;display:flex;align-items:center;justify-content:center;color:#B1BFD6">Chart</div>';
  }

  window.renderPieChart = renderPieChart;
  window.renderBarChart = renderBarChart;
  window.renderSparkline = renderSparkline;
})();

/* notifications.js - notification helpers (attach to window) */

(function () {
  "use strict";

  // Simple toast UI fallback using bootstrap alerts appended to body
  function toast(message, type = 'info', timeout = 3000) {
    try {
      const id = 'toast-' + Math.random().toString(36).slice(2,9);
      const wrapper = document.createElement('div');
      wrapper.id = id;
      wrapper.className = `toast-wrapper position-fixed top-0 end-0 p-3`;
      wrapper.style.zIndex = 2000;
      wrapper.innerHTML = `
        <div class="toast show align-items-center text-bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
          <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
          </div>
        </div>
      `;
      document.body.appendChild(wrapper);
      // remove after timeout
      setTimeout(() => {
        try { wrapper.remove(); } catch (e) {}
      }, timeout + 500);
      return wrapper;
    } catch (e) {
      console.info('toast:', message);
      return null;
    }
  }

  // browser Notification API wrapper
  function notify(title, body) {
    if ("Notification" in window && Notification.permission === "granted") {
      new Notification(title, { body });
    } else if ("Notification" in window && Notification.permission !== "denied") {
      Notification.requestPermission().then(p => {
        if (p === 'granted') new Notification(title, { body });
      });
    } else {
      // fallback to toast
      toast(title + ' — ' + body, 'info', 4000);
    }
  }

  window.toast = toast;
  window.notify = notify;
})();

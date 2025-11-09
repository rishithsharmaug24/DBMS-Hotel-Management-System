/* validation.js - simple client-side validators (attach to window) */

(function () {
  "use strict";

  function required(value) {
    return value !== null && value !== undefined && String(value).trim() !== '';
  }

  function isEmail(value) {
    return /\S+@\S+\.\S+/.test(String(value || ''));
  }

  function isPhone(value) {
    return /^[0-9]{7,15}$/.test(String(value || '').replace(/\s+/g, ''));
  }

  function validateDateOrder(from, to) {
    try {
      const d1 = new Date(from);
      const d2 = new Date(to);
      return !isNaN(d1.valueOf()) && !isNaN(d2.valueOf()) && d2 > d1;
    } catch (e) {
      return false;
    }
  }

  function validateBookingPayload(payload) {
    // minimal checks
    if (!payload) return { ok: false, error: 'Invalid payload' };
    if (!required(payload.guest_id)) return { ok: false, error: 'guest_id required' };
    if (!required(payload.room_id)) return { ok: false, error: 'room_id required' };
    if (!validateDateOrder(payload.check_in, payload.check_out)) return { ok: false, error: 'Invalid dates' };
    return { ok: true };
  }

  // expose
  window.required = required;
  window.isEmail = isEmail;
  window.isPhone = isPhone;
  window.validateDateOrder = validateDateOrder;
  window.validateBookingPayload = validateBookingPayload;
})();

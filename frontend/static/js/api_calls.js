/* api_calls.js - minimal fetch wrappers for your mock API (attach to window) */

(function () {
  "use strict";

  const BASE_URL = ''; // same origin. If using different host, set to e.g. 'http://localhost:5000'

  async function apiFetch(path, options = {}) {
    const url = BASE_URL + path;
    const defaultHeaders = { Accept: 'application/json' };

    if (!options.headers) options.headers = {};
    options.headers = Object.assign({}, defaultHeaders, options.headers);

    const res = await fetch(url, options);
    // try to parse json if present
    const contentType = res.headers.get('content-type') || '';
    const body = contentType.includes('application/json') ? await res.json().catch(() => null) : await res.text().catch(() => null);

    if (!res.ok) {
      const err = new Error('API error: ' + res.status);
      err.status = res.status;
      err.body = body;
      throw err;
    }
    return body;
  }

  async function apiGet(path) {
    return apiFetch(path, { method: 'GET' });
  }

  async function apiPost(path, data) {
    return apiFetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  async function apiPut(path, data) {
    return apiFetch(path, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  async function apiDelete(path) {
    return apiFetch(path, { method: 'DELETE' });
  }

  // expose
  window.apiGet = apiGet;
  window.apiPost = apiPost;
  window.apiPut = apiPut;
  window.apiDelete = apiDelete;
})();

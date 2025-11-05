/* api_calls.js - small wrapper to call backend endpoints; replace BASE_URL with your server */
const BASE_URL = 'http://localhost:4000'; // change as required

async function apiGet(path){
  const res = await fetch(BASE_URL + path, { headers: { 'Accept': 'application/json' } });
  if(!res.ok) throw new Error('API error: ' + res.status);
  return res.json();
}

async function apiPost(path, data){
  const res = await fetch(BASE_URL + path, { method:'POST', headers:{ 'Content-Type':'application/json' }, body: JSON.stringify(data) });
  if(!res.ok) throw new Error('API error: ' + res.status);
  return res.json();
}

export { apiGet, apiPost };

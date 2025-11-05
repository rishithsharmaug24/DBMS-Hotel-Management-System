/* main.js - small runtime utilities & include loader */
(async function(){
  // load server-side includes (if served static, this will load fragments)
  async function include(selector, path){
    const el = document.querySelector(selector);
    if(!el) return;
    try{
      const res = await fetch(path);
      if(res.ok){ el.innerHTML = await res.text(); }
    }catch(e){}
  }

  // auto load includes if placeholders exist
  await include('#include-navbar', '/includes/navbar.html');
  await include('#include-sidebar', '/includes/sidebar.html');
  await include('#include-footer', '/includes/footer.html');
  await include('#include-modals', '/includes/modals.html');

  // small init
  document.getElementById('year')?.innerText = new Date().getFullYear();

  // toast helper
  window.toast = function(msg, type='info', timeout=3500){
    const container = document.getElementById('toastContainer') || document.createElement('div');
    container.id = 'toastContainer'; container.className = 'toast-container';
    if(!document.body.contains(container)) document.body.appendChild(container);
    const t = document.createElement('div'); t.className = 'toast'; t.innerText = msg;
    container.appendChild(t);
    setTimeout(()=>t.remove(), timeout);
  };

  // small event: global search
  document.addEventListener('click', e => {
    if(e.target && e.target.id === 'btnSearch'){
      const q = document.getElementById('topSearch').value.trim();
      if(q) window.location.href = '/search.html?q=' + encodeURIComponent(q);
    }
  });

})();

async function fetchReport(){
  try{
    let r = await fetch('/api/report');
    if(!r.ok) throw new Error('no report');
    return await r.json();
  }catch(e){ return null; }
}

function el(s){return document.querySelector(s)}
function els(s){return document.querySelectorAll(s)}

async function refresh(){
  const email = el('#refresh-email')?.value || '';
  const phone = el('#refresh-phone')?.value || '';
  const user = el('#refresh-user')?.value || '';
  // call refresh endpoint
  const payload = {email: email || undefined, phone: phone || undefined, user: user || undefined};
  const res = await fetch('/api/refresh', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
  const j = await res.json();
  el('#refresh-status').innerText = 'Refresh started (pid: '+(j.pid||'n/a')+') — give it a few seconds, then click Reload.';
}

async function renderAll(){
  const data = await fetchReport();
  if(!data){ el('.content').innerHTML = '<div class="card">No report.json found. Run BROsint to create report.json</div>'; return; }
  // reuse existing renderers from previous version (if present) or show JSON
  if(typeof window.renderEmail === 'function') {
    renderEmail(data);
    renderPhone(data);
    renderSocial(data);
    renderIP(data);
    renderHypo(data);
  } else {
    el('.content').innerHTML = '<pre>'+JSON.stringify(data,null,2)+'</pre>';
  }
}

document.addEventListener('DOMContentLoaded', ()=>{
  els('.tab-btn').forEach(b=>{
    b.addEventListener('click', ()=> {
      els('.tab-btn').forEach(x=>x.classList.remove('active'));
      els('.tab').forEach(x=>x.classList.remove('active'));
      b.classList.add('active');
      document.getElementById(b.dataset.tab).classList.add('active');
    });
  });
  el('#btn-refresh')?.addEventListener('click', refresh);
  el('#reload')?.addEventListener('click', ()=>{ renderAll(); el('#refresh-status').innerText = 'Refreshed'; });
  renderAll();
});

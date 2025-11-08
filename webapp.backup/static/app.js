async function fetchReport(){
  try{
    let r = await fetch('/api/report');
    if(!r.ok) throw new Error('no report');
    return await r.json();
  }catch(e){
    return null;
  }
}

function el(sel){return document.querySelector(sel)}
function els(sel){return document.querySelectorAll(sel)}

function renderEmail(data){
  const box = el('#email'); box.innerHTML='';
  const email = data.query?.email || 'N/A';
  const card = document.createElement('div'); card.className='card';
  card.innerHTML = `<div class="small">Queried Email</div><div>${email}</div>`;
  box.appendChild(card);

  const intel = data.results?.email_intel || {};
  const breaches = intel.breaches || intel.breach_data || [];
  const enrich = intel.enrichment || {};
  const bcard = document.createElement('div'); bcard.className='card';
  bcard.innerHTML = '<div class="small">Breaches</div><div class="pre">'+ (breaches.length? JSON.stringify(breaches, null,2): 'None') +'</div>';
  box.appendChild(bcard);

  const ecard = document.createElement('div'); ecard.className='card';
  ecard.innerHTML = '<div class="small">Enrichment</div><div class="pre">'+ (enrich? JSON.stringify(enrich,null,2): 'None') +'</div>';
  box.appendChild(ecard);
}

function renderPhone(data){
  const box = el('#phone'); box.innerHTML='';
  const phone = data.query?.phone || 'N/A';
  const card = document.createElement('div'); card.className='card';
  card.innerHTML = `<div class="small">Phone</div><div>${phone}</div>`;
  box.appendChild(card);
  const intel = data.results?.phone_intel || {};
  const pcard = document.createElement('div'); pcard.className='card';
  pcard.innerHTML = '<div class="small">Phone Info</div><div class="pre">'+ JSON.stringify(intel,null,2) +'</div>';
  box.appendChild(pcard);
}

function renderSocial(data){
  const box = el('#social'); box.innerHTML='';
  const intel = data.results?.social_intel || {matched_profiles:[]};
  const card = document.createElement('div'); card.className='card';
  card.innerHTML = '<div class="small">Matched Profiles</div><div class="pre">'+ JSON.stringify(intel.matched_profiles || [],null,2) +'</div>';
  box.appendChild(card);
}

function renderIP(data){
  const box = el('#ip'); box.innerHTML='';
  const intel = data.results?.ip_intel || {};
  const card = document.createElement('div'); card.className='card';
  card.innerHTML = '<div class="small">IP & Network</div><div class="pre">'+ JSON.stringify(intel,null,2) +'</div>';
  box.appendChild(card);
}

function renderHypo(data){
  const box = el('#hypo'); box.innerHTML='';
  const h = data.hypothesis || {};
  const levelClass = h.level === 'high' ? 'conf-high' : (h.level === 'medium' ? 'conf-med' : 'conf-low');
  const card = document.createElement('div'); card.className='card';
  card.innerHTML = `<div class="small">Confidence</div><div class="${levelClass}">${h.confidence}% — ${h.level}</div>
    <div class="small">Summary</div><div class="pre">${h.summary}</div>`;
  box.appendChild(card);
}

async function refresh(){
  const data = await fetchReport();
  if(!data){ el('.content').innerHTML = '<div class="card">No report.json found. Run BROsint to create report.json</div>'; return; }
  renderEmail(data);
  renderPhone(data);
  renderSocial(data);
  renderIP(data);
  renderHypo(data);
}

document.addEventListener('DOMContentLoaded', ()=>{
  // tabs
  els('.tab-btn').forEach(b=>{
    b.addEventListener('click', ()=> {
      els('.tab-btn').forEach(x=>x.classList.remove('active'));
      els('.tab').forEach(x=>x.classList.remove('active'));
      b.classList.add('active');
      el('#'+b.dataset.tab).classList.add('active');
    });
  });
  el('#refresh').addEventListener('click', refresh);
  refresh();
});

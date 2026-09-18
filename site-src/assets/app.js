(() => {
  const root = document.documentElement;
  const saved = localStorage.getItem('pw-doc-theme');
  if (saved) root.dataset.theme = saved;
  else if (matchMedia('(prefers-color-scheme: dark)').matches) root.dataset.theme = 'dark';

  document.querySelectorAll('[data-theme-toggle]').forEach(btn => btn.addEventListener('click', () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    localStorage.setItem('pw-doc-theme', next);
  }));


  const rail = document.querySelector('[data-rail]');
  const scrim = document.querySelector('[data-rail-scrim]');
  const closeRail = () => { rail?.classList.remove('open'); scrim?.classList.remove('open'); };
  document.querySelectorAll('[data-menu]').forEach(btn => btn.addEventListener('click', () => {
    rail?.classList.toggle('open');
    scrim?.classList.toggle('open');
  }));
  scrim?.addEventListener('click', closeRail);
  rail?.querySelectorAll('a').forEach(a => a.addEventListener('click', closeRail));

  const modal = document.querySelector('.search-modal');
  const input = document.querySelector('.search-input');
  const results = document.querySelector('.results');
  let index = window.PLAINWIRE_DOC_INDEX || null;
  async function openSearch(){
    modal?.classList.add('open');
    input?.focus();
    if (!index) index = await fetch((document.body.dataset.root || '') + 'search-index.json').then(r=>r.json());
  }
  function closeSearch(){ modal?.classList.remove('open'); if(input) input.value=''; if(results) results.innerHTML=''; }
  document.querySelectorAll('[data-search]').forEach(b=>b.addEventListener('click',openSearch));
  modal?.addEventListener('click',e=>{if(e.target===modal) closeSearch()});
  document.addEventListener('keydown',e=>{
    if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();openSearch()}
    if(e.key==='Escape'){ closeSearch(); closeRail(); }
  });
  input?.addEventListener('input',()=>{
    if(!index) return;
    const q=input.value.trim().toLowerCase();
    if(!q){results.innerHTML='';return}
    const terms=q.split(/\s+/).filter(Boolean);
    const scored=index.map(p=>{
      const hay=(p.title+' '+p.text).toLowerCase();
      let score=terms.reduce((s,t)=>s+(p.title.toLowerCase().includes(t)?12:0)+(hay.includes(t)?2:0),0);
      return [score,p];
    }).filter(x=>x[0]>0).sort((a,b)=>b[0]-a[0]).slice(0,12);
    results.innerHTML=scored.map(([,p])=>`<a class="result" href="${document.body.dataset.root||''}${p.path}"><b>${escapeHtml(p.title)}</b><span>${escapeHtml(p.summary)}</span></a>`).join('') || '<div class="result"><span>No matching page.</span></div>';
  });
  function escapeHtml(s){return s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
})();

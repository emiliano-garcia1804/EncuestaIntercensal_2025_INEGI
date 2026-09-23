'use strict';
const D=window.DASHBOARD_DATA, R=window.POPULATION_REFERENCE, G=window.MAP_DATA;
const $=id=>document.getElementById(id);
const nf=new Intl.NumberFormat('es-MX',{maximumFractionDigits:0});
const fmt=n=>nf.format(n);
const pct=(n,d)=>d?(100*n/d).toFixed(1)+'%':'0.0%';
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const colors=['#087f8c','#5474d3','#a66406','#8b95a5'];
const views={sex:{labels:['Mujeres','Hombres','No especificado / otro'],note:'Sexo según la codificación proporcionada: 1 = mujeres; 3 = hombres. Pendiente de cotejo con el diccionario oficial.'},nat:{labels:['Mexicana','No mexicana','No especificada / otra'],note:'Nacionalidad: 1 = mexicana; 3 = no mexicana; 9 = no especificada. No equivale al país de nacimiento.'},birth:{labels:['Ciudad de México','Otra entidad de México','Extranjero','No especificado'],note:'Lugar de nacimiento: Ciudad de México, otras entidades del país, extranjero y no especificado. Los códigos 997, 998 y 999 se conservan como no especificados.'}};
let view='birth',expanded=false;
if(!D){document.querySelector('main').innerHTML='<h1>No se pudieron cargar los datos</h1><p>Mantén data.js junto a index.html y vuelve a abrir la página.</p>';throw Error('Missing data.js');}
const municipalities=[...D.municipalities].sort((a,b)=>a.name.localeCompare(b.name,'es'));
const targets=allocateTargets(municipalities,R);
const estimated=()=>$('basis').value==='estimate';
const count=n=>(estimated()?'≈ ':'')+fmt(n);
const unit=()=>estimated()?'personas estimadas':'registros';
$('municipality').insertAdjacentHTML('beforeend',municipalities.map(m=>`<option value="${esc(m.code)}">${esc(m.name)}</option>`).join(''));
function selected(){return ($('municipality').value==='all'?municipalities:municipalities.filter(m=>m.code===$('municipality').value)).map(m=>scaledMunicipality(m));}
function combine(rows){const r={n:0,sampleN:0,sex:[0,0,0],nat:[0,0,0],birth:[0,0,0,0],origins:{}};rows.forEach(m=>{r.n+=m.n;r.sampleN+=m.sampleN;['sex','nat','birth'].forEach(k=>m[k].forEach((v,i)=>r[k][i]+=v));Object.entries(m.origins).forEach(([k,v])=>r.origins[k]=(r.origins[k]||0)+v);});return r;}
function render(){const rows=selected(),total=combine(rows),v=views[view],percent=$('scale').value==='percent';
 renderExplorer(rows,total);
 $('definition').textContent=v.note+' Base: '+unit()+'.';
 $('legend').innerHTML=v.labels.map((s,i)=>`<span><i class="dot" style="background:${colors[i]}"></i>${s}</span>`).join('');
 const ordered=[...rows].sort((a,b)=>b.n-a.n),max=Math.max(...rows.map(m=>m.n),1);
 $('comparison').innerHTML=`<div class="axis"><span>Alcaldía</span><div><span>0</span><span>${percent?'100%':fmt(max)}</span></div><span>Total</span></div>`+ordered.map(m=>`<div class="chart-row"><button class="row-name" data-mun="${esc(m.code)}" title="Explorar ${esc(m.name)}">${esc(m.name)}</button><div class="bar" role="img" aria-label="${esc(m.name+': '+v.labels.map((l,i)=>l+' '+count(m[view][i])+' ('+pct(m[view][i],m.n)+')').join(', '))}">${m[view].map((n,i)=>`<span class="segment" title="${v.labels[i]}: ${count(n)} (${pct(n,m.n)})" style="width:${100*n/(percent?m.n:max)}%;background:${colors[i]}">${(n/(percent?m.n:max)>0.17)?(percent?pct(n,m.n):fmt(n)):''}</span>`).join('')}</div><span class="row-total">${count(m.n)}</span></div>`).join('');
 $('comparison').querySelectorAll('[data-mun]').forEach(b=>b.addEventListener('click',()=>{$('municipality').value=b.dataset.mun;expanded=false;render();}));
 $('detail-table').innerHTML=`<caption>${esc(view==='sex'?'Sexo':view==='nat'?'Nacionalidad':'Lugar de nacimiento')} · ${unit()} y porcentaje de cada alcaldía</caption><thead><tr><th scope="col">Alcaldía</th>${v.labels.map(l=>`<th scope="col">${l}</th>`).join('')}<th scope="col">Total</th></tr></thead><tbody>${ordered.map(m=>`<tr><th scope="row">${esc(m.name)}</th>${m[view].map(n=>`<td>${count(n)} (${pct(n,m.n)})</td>`).join('')}<td>${count(m.n)}</td></tr>`).join('')}</tbody>`;
 const scope=$('origin-scope').value,origins=Object.entries(total.origins).map(([code,n])=>({code,n,...D.origins[code]})).filter(o=>scope==='all'||(scope==='mexico'?o.group==='cdmx'||o.group==='mexico':o.group==='abroad')).sort((a,b)=>b.n-a.n||a.name.localeCompare(b.name,'es'));
 const subset=origins.reduce((s,o)=>s+o.n,0),shown=expanded?origins:origins.slice(0,10),originMax=origins[0]?.n||1;
 $('origin-title').textContent='¿Dónde nacieron? · '+(rows.length===16?'Todas las alcaldías':rows[0].name);
 $('origin-description').textContent=`${count(subset)} ${unit()} en este filtro. Se muestran ${shown.length} de ${origins.length} lugares; los porcentajes usan el total de ${count(total.n)} ${unit()} de la selección.`;
 $('origins').innerHTML=shown.length?shown.map(o=>`<div class="origin-row"><div class="origin-label"><span>${esc(o.name)}</span><span>${count(o.n)} · ${pct(o.n,total.n)}</span></div><div class="origin-track"><div class="origin-fill" style="width:${100*o.n/originMax}%;background:${o.group==='abroad'?colors[2]:o.group==='unknown'?colors[3]:colors[0]}"></div></div></div>`).join(''):'<p class="empty">No hay registros para este filtro.</p>';
 $('show-all').hidden=origins.length<=10;$('show-all').textContent=expanded?'Mostrar primeros 10':`Ver los ${origins.length} lugares`;$('show-all').setAttribute('aria-expanded',expanded);
 $('origin-summary').textContent=`En esta selección: ${count(total.nat[2])} ${unit()} sin nacionalidad especificada y ${count(total.birth[3])} con lugar de nacimiento no especificado. Se mantienen dentro del total.`;
}
document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>{view=b.dataset.view;document.querySelectorAll('[data-view]').forEach(x=>{x.classList.toggle('active',x===b);x.setAttribute('aria-pressed',x===b)});render();}));
['municipality','scale','origin-scope','basis','map-metric'].forEach(id=>$(id).addEventListener('change',()=>{if(id!=='scale')expanded=false;render();}));
$('show-all').addEventListener('click',()=>{expanded=!expanded;render();});
initializeReference();
$('footer-source').textContent=D.source+' · '+fmt(D.total)+' registros · estimación propia';render();

const number = n => new Intl.NumberFormat('en-US').format(Math.round(n || 0));
const currency = n => '$' + new Intl.NumberFormat('en-US',{maximumFractionDigits:0}).format(Math.round(n || 0));
let latest = null;
let currentView = 'overview';
const todayLabel=document.getElementById('todayLabel');
if(todayLabel)todayLabel.textContent=new Intl.DateTimeFormat('en-US',{weekday:'long',month:'long',day:'numeric',year:'numeric'}).format(new Date());
function showToast(message){
  const el=document.getElementById('toast');if(!el)return;
  el.textContent=message;el.classList.add('show');
  clearTimeout(showToast.timer);showToast.timer=setTimeout(()=>el.classList.remove('show'),3200);
}
function renderEdaCharts(data){
  const palette=['#5773f0','#9675e7','#40b494','#e7a04e','#ef7896'];
  const regionPie=document.getElementById('regionPie');
  const legend=document.getElementById('regionPieLegend');
  const regions=data.regions||[];
  if(regionPie&&regions.length){
    let start=0;
    const stops=regions.map((region,index)=>{
      const share=Math.max(0,Number(region.share)||0);const stop=start+share;
      const segment=`${palette[index%palette.length]} ${start}% ${stop}%`;start=stop;return segment;
    });
    regionPie.style.background=`conic-gradient(${stops.join(',')})`;
    document.getElementById('pieCenter').innerHTML=`${regions[0].share}%<span>${regions[0].region}</span>`;
    legend.innerHTML=regions.map((region,index)=>`<div class="pie-legend-row"><i style="width:8px;height:8px;border-radius:50%;background:${palette[index%palette.length]}"></i><span>${region.region}</span><b>${region.share}%</b></div>`).join('');
  }else if(legend){
    legend.innerHTML='<div class="empty-chart">No regional data for this period.</div>';
  }
  const histogram=document.getElementById('orderHistogram');
  const bins=data.histogram||[];const max=Math.max(...bins.map(bin=>bin.orders),1);
  if(histogram){
    histogram.innerHTML=bins.length?bins.map(bin=>`<div class="hist-bin"><span class="hist-count">${number(bin.orders)}</span><i class="hist-bar" style="height:${Math.max(3,bin.orders/max*82)}%" title="${bin.bucket}: ${number(bin.orders)} orders"></i><span class="hist-label">${bin.bucket}</span></div>`).join(''):'<div class="empty-chart">No orders for these filters.</div>';
  }
}
async function loadDashboard(){
  const days=document.getElementById('period')?.value||30;
  const region=document.getElementById('regionFilter')?.value||'all';
  try{
    const response=await fetch(`/api/overview?days=${encodeURIComponent(days)}&region=${encodeURIComponent(region)}`);
    if(!response.ok) throw new Error('Dashboard request failed');
    latest=await response.json();
    const m=latest.metrics;
    document.getElementById('revenue').textContent=currency(m.revenue);
    document.getElementById('orders').textContent=number(m.orders);
    document.getElementById('aov').textContent='$'+Number(m.aov).toFixed(2);
    document.getElementById('retention').textContent=Number(m.returning_rate).toFixed(1)+'%';
    document.querySelector('.source-top span').textContent='SQL database connected';
    document.querySelector('.source-sub').textContent=`${number(m.orders)} orders · updated just now`;
    document.querySelector('.refresh').textContent='Live SQL data';
    document.querySelector('.insight p').innerHTML=`<b>${latest.insights.top_region}</b> is the top region. <b>${latest.insights.top_product}</b> leads products with <b>${currency(latest.insights.top_product_revenue)}</b> revenue.`;
    const regionBox=document.getElementById('regionBreakdown');
    const colors=['#5773f0','#9675e7','#40b494','#e7a04e'];
    regionBox.innerHTML=latest.regions.map((r,i)=>`<div class="break-row"><div class="break-name"><i style="display:inline-block;width:7px;height:7px;border-radius:50%;background:${colors[i%colors.length]};margin-right:7px"></i>${r.region}</div><div class="break-val">${currency(r.revenue)}</div><div class="bar"><i style="width:${r.share}%;background:${colors[i%colors.length]}"></i></div></div>`).join('')||'<div class="panel-sub">No rows match these filters.</div>';
    const productRows=document.getElementById('productRows');
    productRows.innerHTML=latest.products.slice(0,5).map((p,i)=>`<tr><td class="product"><i class="prod-dot">${['◈','▧','◉','◇','▱'][i%5]}</i>${p.product}</td><td>${p.category}</td><td>${number(p.units)}</td><td>${currency(p.revenue)}</td><td><span class="pill">SQL</span></td></tr>`).join('');
    renderEdaCharts(latest);
    const daily=latest.daily;
    if(daily.length>1){
      const max=Math.max(...daily.map(r=>r.revenue),1), min=Math.min(...daily.map(r=>r.revenue));
      const x=i=>48+i*(587/(daily.length-1)), y=v=>170-(v/max)*132;
      const line=daily.map((r,i)=>(i?'L':'M')+x(i)+' '+y(r.revenue)).join(' ');
      document.getElementById('revenueLine').setAttribute('d',line);
      document.getElementById('revenueArea').setAttribute('d',line+` L ${x(daily.length-1)} 180 L ${x(0)} 180 Z`);
      const ol=daily.map((r,i)=>(i?'L':'M')+x(i)+' '+y(r.orders*max/Math.max(...daily.map(d=>d.orders),1))).join(' ');
      document.getElementById('ordersLine').setAttribute('d',ol);
      document.getElementById('ordersArea').setAttribute('d',ol+` L ${x(daily.length-1)} 180 L ${x(0)} 180 Z`);
      document.getElementById('chartPoints').innerHTML=daily.map((r,i)=>`<circle cx="${x(i)}" cy="${y(r.revenue)}" r="2" fill="#5571ee"><title>${r.order_date}: ${currency(r.revenue)} · ${number(r.orders)} orders</title></circle>`).join('');
      const labels=document.getElementById('chartLabels');labels.innerHTML='';
      [0,Math.floor((daily.length-1)/3),Math.floor((daily.length-1)*2/3),daily.length-1].forEach(i=>{const d=new Date(daily[i].order_date+'T12:00:00');labels.innerHTML+=`<text class="axis" x="${x(i)-14}" y="205">${d.toLocaleDateString('en-US',{month:'short',day:'numeric'})}</text>`});
      const grid=document.getElementById('chartGrid');grid.querySelectorAll('.gridline').forEach(el=>{const pos=Number(el.getAttribute('y1'));const value=Math.round((170-pos)/132*max);const text=el.nextElementSibling;if(text)text.textContent='$'+Math.round(value/1000)+'k'});
    }
    renderDataView(currentView);
  }catch(err){
    const source=document.querySelector('.source-top span');if(source)source.textContent='SQL data unavailable';
    console.error(err);
  }
}
// Dashboard controls trigger SQL-backed refreshes.
document.getElementById('period').addEventListener('change',loadDashboard);
document.getElementById('regionFilter').addEventListener('change',loadDashboard);
window.ask=async function(question){
  const q=String(question||'').trim();if(!q)return;
  appendMessage(q,'user');document.getElementById('question').value='';
  try{
    const response=await fetch('/api/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q,days:Number(document.getElementById('period').value),region:document.getElementById('regionFilter').value})});
    const data=await response.json();if(!response.ok)throw new Error(data.error||'Could not answer that question.');
    appendMessage(`${data.answer}\n\n${data.source}`,'bot');
  }catch(err){appendMessage('I could not reach the analysis service. Check that the Python server is running.','bot')}
};
function appendMessage(text,who){
  const bubble=document.createElement('div');bubble.className=`message ${who}`;bubble.textContent=text;
  const messages=document.getElementById('messages');messages.appendChild(bubble);messages.scrollTop=messages.scrollHeight;
}
function showSqlDialog(){document.getElementById('sqlModal').classList.add('open');}
function hideSqlDialog(){document.getElementById('sqlModal').classList.remove('open');}
function setChatOpen(open){
  const panel=document.getElementById('chat');panel.classList.toggle('open',open);
  if(open)setTimeout(()=>document.getElementById('question').focus(),80);
}
function exportProductCsv(){
  if(!latest)return;
  const rows=[['Product','Category','Units','Revenue'],...latest.products.map(p=>[p.product,p.category,p.units,p.revenue])];
  const csv=rows.map(r=>r.map(v=>'"'+String(v).replaceAll('"','""')+'"').join(',')).join('\n');
  const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));a.download='northstar-products.csv';a.click();URL.revokeObjectURL(a.href);showToast('Product data exported as CSV.');
}
// The existing chat form and suggested prompts call the global ask function above.
window.addEventListener('DOMContentLoaded',loadDashboard);
loadDashboard();

window.switchView = function(key) {
  const labels = {
    overview: ['Revenue overview', 'Overview'],
    products: ['Product performance', 'Products'],
    customers: ['Customer insights', 'Customers'],
    regions: ['Regional analysis', 'Regions'],
    reports: ['Saved reports', 'Saved reports']
  };
  if (!labels[key]) return;
  currentView = key;
  document.querySelectorAll('#navigation button').forEach(button => button.classList.toggle('active', button.dataset.view === key));
  const overview = document.getElementById('overview');
  const other = document.getElementById('otherView');
  overview.classList.toggle('active', key === 'overview');
  other.classList.toggle('active', key !== 'overview');
  document.getElementById('viewTitle').textContent = labels[key][0];
  document.getElementById('crumb').textContent = labels[key][1];
  document.getElementById('otherTitle').textContent = labels[key][0];
  renderDataView(key);
};
// Handle the sidebar at the navigation container so every item, including icon-only
// items on narrow screens, reliably selects its view.
document.getElementById('navigation')?.addEventListener('click', event => {
  const button = event.target.closest('button[data-view]');
  if (!button) return;
  event.preventDefault();
  event.stopPropagation();
  event.stopImmediatePropagation();
  window.switchView(button.dataset.view);
}, true);

function renderDataView(key) {
  if (key === 'overview' || !latest) return;
  const target = document.getElementById('otherContent');
  if (!target) return;
  const m = latest.metrics;
  if (key === 'products') {
    target.innerHTML = `<table class="table"><thead><tr><th>Product</th><th>Category</th><th>Units</th><th>Revenue</th></tr></thead><tbody>${latest.products.map(p => `<tr><td class="product">${p.product}</td><td>${p.category}</td><td>${number(p.units)}</td><td>${currency(p.revenue)}</td></tr>`).join('')}</tbody></table><button class="secondary" data-export="products">Export product CSV</button>`;
  } else if (key === 'regions') {
    target.innerHTML = `<table class="table"><thead><tr><th>Region</th><th>Orders</th><th>Revenue</th><th>Share</th></tr></thead><tbody>${latest.regions.map(r => `<tr><td class="product">${r.region}</td><td>${number(r.orders)}</td><td>${currency(r.revenue)}</td><td>${r.share}%</td></tr>`).join('')}</tbody></table><button class="secondary" onclick="exportRegionsCsv()">Export region CSV</button>`;
  } else if (key === 'customers') {
    target.innerHTML = `<div class="grid" style="margin-top:12px"><div class="card kpi"><div class="kpi-head">Distinct customers</div><div class="kpi-value">${number(m.customers)}</div></div><div class="card kpi"><div class="kpi-head">Returning order rate</div><div class="kpi-value">${Number(m.returning_rate).toFixed(1)}%</div></div><div class="card kpi"><div class="kpi-head">Average order value</div><div class="kpi-value">${currency(m.aov)}</div></div><div class="card kpi"><div class="kpi-head">Orders in selection</div><div class="kpi-value">${number(m.orders)}</div></div></div><p class="panel-sub">These figures follow the selected date and region filters.</p>`;
  } else if (key === 'reports') {
    target.innerHTML = `<div style="display:grid;gap:10px;margin-top:12px"><div class="insight"><b>Revenue overview</b><p>${currency(m.revenue)} revenue across ${number(m.orders)} orders · current filters</p><button class="secondary" data-report="overview">Preview summary</button></div><div class="insight"><b>Product performance</b><p>${latest.products.length} products ranked by sales revenue.</p><button class="secondary" data-report="products">Preview products</button></div><div class="insight"><b>Regional scorecard</b><p>${latest.regions.length} regions compared by revenue share.</p><button class="secondary" data-report="regions">Preview regions</button></div></div>`;
  }
}

function exportRegionsCsv() {
  if (!latest) return;
  const rows = [['Region', 'Orders', 'Revenue', 'Share'], ...latest.regions.map(r => [r.region, r.orders, r.revenue, r.share + '%'])];
  const csv = rows.map(r => r.map(v => '"' + String(v).replaceAll('"', '""') + '"').join(',')).join('\n');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([csv], {type: 'text/csv'}));
  a.download = 'northstar-regions.csv'; a.click(); URL.revokeObjectURL(a.href);
  showToast('Region data exported as CSV.');
}

async function checkDatabase() {
  const button = document.querySelector('#sqlModal .primary');
  button.disabled = true; button.textContent = 'Checking…';
  try {
    const response = await fetch('/api/health');
    const state = await response.json();
    if (!response.ok || !state.ok) throw new Error('Database did not respond');
    showToast(`Database connected: ${state.database}${state.ai_enabled ? ' · AI enabled' : ' · offline assistant'}`);
    hideSqlDialog();
  } catch (error) {
    showToast('Could not reach the data service. Restart python app.py and try again.');
  } finally {
    button.disabled = false; button.textContent = 'Check connection';
  }
}

document.getElementById('notificationsButton')?.addEventListener('click', () => {
  document.querySelector('#notificationsButton .notify-dot')?.remove();
  showToast('You’re all caught up. Dashboard data is up to date.');
});
document.getElementById('regionExportButton')?.addEventListener('click', exportRegionsCsv);
document.getElementById('connectSqlButton')?.addEventListener('click', showSqlDialog);
document.getElementById('manageSqlButton')?.addEventListener('click', showSqlDialog);
document.getElementById('closeSqlButton')?.addEventListener('click', hideSqlDialog);
document.getElementById('testDbButton')?.addEventListener('click', checkDatabase);
document.getElementById('exportCsvButton')?.addEventListener('click', exportProductCsv);
document.getElementById('viewProductsButton')?.addEventListener('click', () => window.switchView('products'));
document.getElementById('quickAskButton')?.addEventListener('click', () => setChatOpen(true));
document.getElementById('aiFab')?.addEventListener('click', () => setChatOpen(!document.getElementById('chat').classList.contains('open')));
document.getElementById('closeChatButton')?.addEventListener('click', () => setChatOpen(false));
document.querySelectorAll('.suggestion[data-question]').forEach(button => {
  button.addEventListener('click', () => {setChatOpen(true);window.ask(button.dataset.question);});
});
document.getElementById('chatForm')?.addEventListener('submit',event=>{
  event.preventDefault();event.stopImmediatePropagation();window.ask(document.getElementById('question').value);
},true);
document.getElementById('otherContent')?.addEventListener('click', event => {
  const exportButton=event.target.closest('[data-export="products"]');
  if(exportButton){exportProductCsv();return;}
  const button = event.target.closest('[data-report]');
  if (!button) return;
  const report = button.dataset.report;
  if (report === 'products') window.switchView('products');
  else if (report === 'regions') window.switchView('regions');
  else { window.switchView('overview'); showToast('Revenue overview is shown with the current filters.'); }
});

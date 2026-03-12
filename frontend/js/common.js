// ============ COMMON UTILITIES ============
const API = '';

function fmt(n, decimals=0) {
  if (n === null || n === undefined) return 'Rs. 0';
  return 'Rs. ' + parseFloat(n).toLocaleString('en-IN', {minimumFractionDigits: decimals, maximumFractionDigits: decimals});
}

function fmtNum(n, d=2) {
  return parseFloat(n || 0).toLocaleString('en-IN', {minimumFractionDigits: d, maximumFractionDigits: d});
}

function showToast(msg, type='success') {
  let c = document.getElementById('toastContainer');
  if (!c) {
    c = document.createElement('div');
    c.id = 'toastContainer';
    c.className = 'toast-container';
    document.body.appendChild(c);
  }
  const t = document.createElement('div');
  const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
  t.className = `toast ${type}`;
  t.innerHTML = `<span>${icon}</span><span>${msg}</span>`;
  c.appendChild(t);
  setTimeout(() => { t.style.opacity='0'; t.style.transform='translateX(30px)'; t.style.transition='0.3s'; setTimeout(() => t.remove(), 300); }, 3000);
}

async function api(url, method='GET', body=null) {
  const opts = {
    method,
    headers: {'Content-Type': 'application/json'},
    credentials: 'include'
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(API + url, opts);
  const data = await res.json();
  return data;
}

function confirm_delete(msg='Delete this record?') {
  return new Promise(resolve => {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay active';
    overlay.innerHTML = `
      <div class="modal" style="max-width:360px">
        <div class="modal-header"><span class="modal-title">⚠️ Confirm Delete</span></div>
        <div class="modal-body"><p style="color:var(--text-muted)">${msg}</p></div>
        <div class="modal-footer">
          <button class="btn btn-secondary" id="cancelDel">Cancel</button>
          <button class="btn btn-danger" id="confirmDel">Delete</button>
        </div>
      </div>`;
    document.body.appendChild(overlay);
    overlay.querySelector('#cancelDel').onclick = () => { overlay.remove(); resolve(false); };
    overlay.querySelector('#confirmDel').onclick = () => { overlay.remove(); resolve(true); };
  });
}

// Nepal BS months
const BS_MONTHS = ['Baisakh','Jestha','Ashadh','Shrawan','Bhadra','Ashwin','Kartik','Mangsir','Poush','Magh','Falgun','Chaitra'];

// Get current BS date (approximate)
function getCurrentBSDate() {
  const now = new Date();
  // AD year + 56 or 57 (based on month)
  const adY = now.getFullYear();
  const adM = now.getMonth() + 1; // 1-based
  const bsY = adM > 3 ? adY + 57 : adY + 56;
  const bsM = adM > 3 ? adM - 3 : adM + 9;
  const bsD = now.getDate();
  return {
    year: bsY,
    month: bsM,
    day: bsD,
    month_name: BS_MONTHS[bsM - 1],
    date_str: `${bsY}-${String(bsM).padStart(2,'0')}-${String(bsD).padStart(2,'0')}`,
    date_ad: now.toISOString().split('T')[0]
  };
}

function getMonthName(m) { return BS_MONTHS[(m-1)] || ''; }

function buildSidebar(activePage) {
  const navItems = [
    { href: 'dashboard.html', icon: '📊', label: 'Dashboard', section: 'Main' },
    { href: 'income.html', icon: '💵', label: 'Income', section: 'Transactions' },
    { href: 'expense.html', icon: '💳', label: 'Expenditure', section: '' },
    { href: 'networth.html', icon: '📈', label: 'Net Worth', section: '' },
    { href: 'loan.html', icon: '🤝', label: 'Loans', section: '' },
    { href: 'share.html', icon: '📉', label: 'Share Portfolio', section: 'Investments' },
    { href: 'bike.html', icon: '🏍️', label: 'Bike', section: 'Vehicle' },
    { href: 'petrol.html', icon: '⛽', label: 'Petrol', section: '' },
    { href: 'baby.html', icon: '👶', label: 'Baby', section: 'Family' },
    { href: 'reports.html', icon: '📋', label: 'Reports', section: 'Reports' },
    { href: 'settings.html', icon: '⚙️', label: 'Settings', section: 'Other' },
  ];
  let html = '';
  let lastSection = '';
  navItems.forEach(item => {
    if (item.section && item.section !== lastSection) {
      html += `<div class="nav-section-title">${item.section}</div>`;
      lastSection = item.section;
    }
    const isActive = activePage && item.href.includes(activePage);
    html += `<a href="${item.href}" class="nav-item${isActive ? ' active' : ''}">
      <span class="nav-icon">${item.icon}</span>${item.label}</a>`;
  });
  return html;
}

async function logout() {
  await fetch('/api/auth/logout', {method:'POST', credentials:'include'});
  window.location.href = '/login.html';
}

// Format currency for display
function formatCurrency(val) {
  const n = parseFloat(val) || 0;
  if (n >= 10000000) return `Rs. ${(n/10000000).toFixed(2)}Cr`;
  if (n >= 100000) return `Rs. ${(n/100000).toFixed(2)}L`;
  return fmt(n);
}

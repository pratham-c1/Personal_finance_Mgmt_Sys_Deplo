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
  setTimeout(() => {
    t.style.opacity = '0';
    t.style.transform = 'translateX(30px)';
    t.style.transition = '0.3s';
    setTimeout(() => t.remove(), 300);
  }, 3000);
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
    overlay.querySelector('#cancelDel').onclick  = () => { overlay.remove(); resolve(false); };
    overlay.querySelector('#confirmDel').onclick = () => { overlay.remove(); resolve(true); };
  });
}

// BS months
const BS_MONTHS = ['Baisakh','Jestha','Ashadh','Shrawan','Bhadra','Ashwin','Kartik','Mangsir','Poush','Magh','Falgun','Chaitra'];

// ── AD → BS conversion ────────────────────────────────────────────────────────
// Method: anchor on verified Baisakh 1 dates + official month-length data.
// Verified anchor: 1 Baisakh 2082 BS = 13 April 2025 AD (confirmed standard).
// Cross-checked: 29 Falgun 2082 = 13 March 2026 (user-confirmed).
//
// BAISAKH1_AD[y] = the AD date string of 1 Baisakh of BS year y.
// Verified from official Nepal government calendar for 2078-2083;
// 2084+ computed from month-length data below.
const _B1 = {
  2078:'2021-04-14', 2079:'2022-04-14', 2080:'2023-04-14',
  2081:'2024-04-13', 2082:'2025-04-13', 2083:'2026-04-13',
};

// Verified month lengths (days per month, Baisakh→Chaitra).
// 2082 verified by: months 1-10 sum=306, Falgun=30, Chaitra=29, total=365.
// Cross-checked against Baisakh 1 date pairs for each year.
const _MD = {
  2078:[31,31,32,31,31,31,30,29,30,29,30,30], // 365
  2079:[31,31,32,31,32,30,30,29,30,29,30,30], // 365
  2080:[31,32,31,32,31,30,30,30,29,29,30,30], // 365
  2081:[31,31,32,32,31,30,30,29,30,29,30,30], // 365
  2082:[31,32,31,32,31,30,30,29,30,30,30,29], // 365 ✓ (Falgun29=Mar13 2026)
  2083:[31,32,31,32,31,30,30,29,30,29,30,30], // 365
  2084:[31,32,31,32,31,30,30,30,29,30,29,31], // 366
  2085:[31,31,32,31,32,30,30,29,30,29,30,30], // 365
  2086:[31,32,31,32,31,30,30,30,29,30,29,31], // 366
  2087:[31,31,32,31,31,31,30,29,30,29,30,30], // 365
  2088:[31,31,32,32,31,30,30,29,30,29,30,30], // 365
  2089:[31,32,31,32,31,30,30,30,29,29,30,31], // 366
  2090:[31,31,32,31,31,30,30,29,30,29,30,31], // 365
};

// Pre-compute Baisakh 1 dates for 2084+ from month data
(function() {
  let d = new Date(_B1[2083]);
  for (let y = 2083; y <= 2089; y++) {
    const days = (_MD[y]||[]).reduce((a,b)=>a+b,0);
    d = new Date(d.getTime() + days * 86400000);
    _B1[y+1] = d.toISOString().split('T')[0];
  }
})();

function adToBs(adDate) {
  // Use YYYY-MM-DD string comparison (lexicographic = chronological for ISO dates)
  const adStr = adDate.toISOString().split('T')[0];

  // Find which BS year this falls in
  let bsYear = 2078;
  for (let y = 2078; y <= 2090; y++) {
    const nextStart = _B1[y + 1];
    if (!nextStart || adStr < nextStart) { bsYear = y; break; }
  }

  // Days elapsed since Baisakh 1 of that year
  const b1 = new Date(_B1[bsYear]);
  let offset = Math.round((adDate - b1) / 86400000); // Math.round avoids DST ±1h glitch

  // Walk through months
  const months = _MD[bsYear] || [];
  for (let m = 0; m < 12; m++) {
    if (offset < months[m]) return { year: bsYear, month: m + 1, day: offset + 1 };
    offset -= months[m];
  }
  // Fallback (shouldn't happen within covered range)
  return { year: bsYear, month: 12, day: offset + 1 };
}

function getCurrentBSDate() {
  // Use Nepal local date (UTC+5:45) so the date flips at Nepal midnight, not UTC midnight
  const now    = new Date();
  const nplMs  = now.getTime() + (5 * 60 + 45) * 60000; // shift to Nepal time
  const nplDay = new Date(nplMs);
  // Strip time: use date portion only
  const adStr  = nplDay.toISOString().split('T')[0];
  const bs     = adToBs(new Date(adStr));
  return {
    year:       bs.year,
    month:      bs.month,
    day:        bs.day,
    month_name: BS_MONTHS[bs.month - 1],
    date_str:   `${bs.year}-${String(bs.month).padStart(2,'0')}-${String(bs.day).padStart(2,'0')}`,
    date_ad:    adStr
  };
}

function getMonthName(m) { return BS_MONTHS[(m-1)] || ''; }

// ── Format currency ───────────────────────────────────────────────────────────
function formatCurrency(val) {
  const n = parseFloat(val) || 0;
  if (n >= 10000000) return `Rs. ${(n/10000000).toFixed(2)}Cr`;
  if (n >= 100000)   return `Rs. ${(n/100000).toFixed(2)}L`;
  return fmt(n);
}

// ── Auth ──────────────────────────────────────────────────────────────────────
async function logout() {
  await fetch('/api/auth/logout', {method:'POST', credentials:'include'});
  window.location.href = '/login.html';
}

// ── Session cache ─────────────────────────────────────────────────────────────
async function checkAndStoreSession() {
  try {
    const auth = await fetch('/api/auth/check', {credentials: 'include'});
    const data = await auth.json();
    if (data.logged_in) {
      sessionStorage.setItem('pf_role',     data.role     || '');
      sessionStorage.setItem('pf_username', data.username || '');
    }
  } catch(e) {}
}
checkAndStoreSession();

// ── Sidebar builder ───────────────────────────────────────────────────────────
function buildSidebar(activePage) {
  const role     = sessionStorage.getItem('pf_role')     || '';
  const username = sessionStorage.getItem('pf_username') || '';

  const navItems = [
    { href: 'dashboard.html', icon: '📊', label: 'Dashboard',       section: 'Main' },
    { href: 'income.html',    icon: '💵', label: 'Income',           section: 'Transactions' },
    { href: 'expense.html',   icon: '💳', label: 'Expenditure',      section: '' },
    { href: 'networth.html',  icon: '📈', label: 'Net Worth',        section: '' },
    { href: 'loan.html',      icon: '🤝', label: 'Loans',            section: '' },
    { href: 'share.html',     icon: '📉', label: 'Share Portfolio',  section: 'Investments' },
    { href: 'bike.html',      icon: '🏍️', label: 'Bike',             section: 'Vehicle' },
    { href: 'petrol.html',    icon: '⛽', label: 'Petrol',           section: '' },
    { href: 'baby.html',      icon: '👶', label: 'Baby',             section: 'Family' },
    { href: 'reports.html',   icon: '📋', label: 'Reports',          section: 'Reports' },
    { href: 'settings.html',  icon: '⚙️', label: 'Settings',         section: 'Other' },
  ];

  if (role === 'admin') {
    navItems.push({ href: 'users.html', icon: '👥', label: 'Manage Users', section: '' });
  }

  let navHtml = '';
  let lastSection = '';
  navItems.forEach(item => {
    if (item.section && item.section !== lastSection) {
      navHtml += `<div class="nav-section-title">${item.section}</div>`;
      lastSection = item.section;
    }
    const isActive = activePage && item.href.includes(activePage);
    navHtml += `<a href="${item.href}" class="nav-item${isActive ? ' active' : ''}" onclick="closeSidebar()">
      <span class="nav-icon">${item.icon}</span>${item.label}</a>`;
  });

  const html = `
    <nav class="sidebar" id="sidebar">
      <div class="sidebar-logo">
        <div class="logo-icon">💰</div>
        <div class="logo-text">
          <h2>Finance</h2>
          <span>${username ? '@' + username : 'Personal Finance'}</span>
        </div>
      </div>
      <div class="nav-links">${navHtml}</div>
      <div class="sidebar-footer">
        <button class="btn btn-secondary btn-full btn-sm" onclick="logout()">🚪 Sign Out</button>
      </div>
    </nav>`;

  const container = document.getElementById('sidebar-container');
  if (container) container.innerHTML = html;
  return html;
}

// ── Mobile sidebar toggle ─────────────────────────────────────────────────────
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  const btn     = document.getElementById('hamburgerBtn');
  if (!sidebar) return;
  const isOpen = sidebar.classList.contains('open');
  if (isOpen) {
    sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('active');
    if (btn) btn.setAttribute('aria-expanded', 'false');
  } else {
    sidebar.classList.add('open');
    if (overlay) overlay.classList.add('active');
    if (btn) btn.setAttribute('aria-expanded', 'true');
  }
}

function closeSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  const btn     = document.getElementById('hamburgerBtn');
  if (!sidebar) return;
  sidebar.classList.remove('open');
  if (overlay) overlay.classList.remove('active');
  if (btn) btn.setAttribute('aria-expanded', 'false');
}

// Close sidebar on Escape key
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeSidebar(); });

// Close sidebar when window resizes to desktop width
window.addEventListener('resize', () => {
  if (window.innerWidth > 767) closeSidebar();
});

/* algo-pen — Dosimetria Penal Brasil */
(function () {
  'use strict';

  let crimes = [];
  let filtered = [];
  let currentPage = 1;
  let sortField = 'lei';
  let sortDir = 'asc';
  let selectedCrime = null;
  const PAGE_SIZE = 50;

  // ─── Init ────────────────────────────────────────────────────────────────
  async function init() {
    const res = await fetch('data/crimes.json');
    crimes = await res.json();
    filtered = [...crimes];

    populateFilters();
    renderTable();
    renderStats();
    bindEvents();
    updateResultCount();
  }

  // ─── Navigation ──────────────────────────────────────────────────────────
  function bindEvents() {
    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', e => {
        e.preventDefault();
        const tab = link.dataset.tab;
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
        link.classList.add('active');
        document.getElementById(tab).classList.add('active');
      });
    });

    // Search
    const searchInput = document.getElementById('search-input');
    let debounceTimer;
    searchInput.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => { applyFilters(); }, 200);
    });

    // Filters
    document.querySelectorAll('.filters select').forEach(sel => {
      sel.addEventListener('change', applyFilters);
    });

    document.getElementById('btn-clear-filters').addEventListener('click', () => {
      searchInput.value = '';
      document.querySelectorAll('.filters select').forEach(s => s.value = '');
      applyFilters();
    });

    // Sort
    document.querySelectorAll('.sortable').forEach(th => {
      th.addEventListener('click', () => {
        const field = th.dataset.sort;
        if (sortField === field) {
          sortDir = sortDir === 'asc' ? 'desc' : 'asc';
        } else {
          sortField = field;
          sortDir = 'asc';
        }
        renderTable();
      });
    });

    // Dosimetria
    document.querySelectorAll('.circ-judicial, #agravantes, #atenuantes, #aumento, #diminuicao')
      .forEach(el => el.addEventListener('change', calcDosimetria));
    document.querySelectorAll('#agravantes, #atenuantes, #aumento, #diminuicao')
      .forEach(el => el.addEventListener('input', calcDosimetria));

    // Dosimetria crime search
    const dosiSearch = document.getElementById('dosi-crime-search');
    dosiSearch.addEventListener('input', () => {
      const q = dosiSearch.value.toLowerCase().trim();
      const results = document.getElementById('dosi-crime-results');
      if (q.length < 2) { results.classList.remove('visible'); return; }
      const matches = crimes.filter(c =>
        c.crime.toLowerCase().includes(q) ||
        c.artigo.toLowerCase().includes(q)
      ).slice(0, 15);
      results.innerHTML = matches.map(c =>
        `<div class="dosi-result-item" data-id="${c.id}">
          <strong>${c.crime}</strong> — ${c.artigo} (${c.lei}) — ${formatPena(c.pena_min)}–${formatPena(c.pena_max)}
        </div>`
      ).join('');
      results.classList.add('visible');
      results.querySelectorAll('.dosi-result-item').forEach(item => {
        item.addEventListener('click', () => selectCrimeForDosi(+item.dataset.id));
      });
    });
  }

  function selectCrimeForDosi(id) {
    selectedCrime = crimes.find(c => c.id === id);
    const sel = document.getElementById('dosi-crime-selected');
    sel.innerHTML = `<strong>${selectedCrime.crime}</strong><br>${selectedCrime.artigo} (${selectedCrime.lei})<br>Pena: ${formatPena(selectedCrime.pena_min)} a ${formatPena(selectedCrime.pena_max)} de ${selectedCrime.tipo_pena}`;
    sel.classList.add('visible');
    document.getElementById('dosi-crime-results').classList.remove('visible');
    calcDosimetria();
  }

  // ─── Filters ─────────────────────────────────────────────────────────────
  function populateFilters() {
    const leis = [...new Set(crimes.map(c => c.lei))].sort();
    const select = document.getElementById('filter-lei');
    leis.forEach(lei => {
      const opt = document.createElement('option');
      opt.value = lei;
      opt.textContent = lei;
      select.appendChild(opt);
    });
  }

  function applyFilters() {
    const query = document.getElementById('search-input').value.toLowerCase().trim();
    const lei = document.getElementById('filter-lei').value;
    const hediondo = document.getElementById('filter-hediondo').value;
    const elemento = document.getElementById('filter-elemento').value;
    const violencia = document.getElementById('filter-violencia').value;
    const tipoPena = document.getElementById('filter-pena').value;

    filtered = crimes.filter(c => {
      if (query && !(
        c.crime.toLowerCase().includes(query) ||
        c.artigo.toLowerCase().includes(query) ||
        c.lei.toLowerCase().includes(query) ||
        c.obs.toLowerCase().includes(query)
      )) return false;
      if (lei && c.lei !== lei) return false;
      if (hediondo && c.hediondo !== hediondo) return false;
      if (elemento && c.elemento !== elemento) return false;
      if (violencia === 'violencia' && c.violencia !== 'Sim') return false;
      if (violencia === 'grave_ameaca' && c.grave_ameaca !== 'Sim') return false;
      if (violencia === 'ambos' && !(c.violencia === 'Sim' && c.grave_ameaca === 'Sim')) return false;
      if (tipoPena && c.tipo_pena !== tipoPena) return false;
      return true;
    });

    currentPage = 1;
    renderTable();
    updateResultCount();
  }

  function updateResultCount() {
    document.getElementById('result-count').textContent =
      `${filtered.length} de ${crimes.length} tipos`;
  }

  // ─── Table ───────────────────────────────────────────────────────────────
  function renderTable() {
    const sorted = [...filtered].sort((a, b) => {
      let va = a[sortField], vb = b[sortField];
      if (typeof va === 'number') return sortDir === 'asc' ? va - vb : vb - va;
      va = (va || '').toString().toLowerCase();
      vb = (vb || '').toString().toLowerCase();
      return sortDir === 'asc' ? va.localeCompare(vb) : vb.localeCompare(va);
    });

    const start = (currentPage - 1) * PAGE_SIZE;
    const page = sorted.slice(start, start + PAGE_SIZE);

    const tbody = document.getElementById('crimes-tbody');
    tbody.innerHTML = page.map(c => {
      let rowClass = '';
      if (c.hediondo === 'Sim') rowClass = 'hediondo';
      else if (c.violencia === 'Sim' || c.grave_ameaca === 'Sim') rowClass = 'violencia';

      return `<tr class="${rowClass}">
        <td>${c.lei}</td>
        <td>${c.artigo}</td>
        <td>${c.crime}</td>
        <td class="pena-cell">${formatPena(c.pena_min)}</td>
        <td class="pena-cell">${formatPena(c.pena_max)}</td>
        <td><span class="badge ${c.tipo_pena === 'Reclusão' ? 'badge-reclusao' : 'badge-detencao'}">${c.tipo_pena || '—'}</span></td>
        <td>${c.hediondo === 'Sim' ? '<span class="badge badge-hediondo">H</span>' : ''}</td>
      </tr>`;
    }).join('');

    // Update sort indicators
    document.querySelectorAll('.sortable').forEach(th => {
      th.classList.remove('sorted-asc', 'sorted-desc');
      if (th.dataset.sort === sortField) {
        th.classList.add(sortDir === 'asc' ? 'sorted-asc' : 'sorted-desc');
      }
    });

    renderPagination(sorted.length);
  }

  function renderPagination(total) {
    const totalPages = Math.ceil(total / PAGE_SIZE);
    const pag = document.getElementById('pagination');
    if (totalPages <= 1) { pag.innerHTML = ''; return; }

    let html = `<button ${currentPage === 1 ? 'disabled' : ''} data-page="${currentPage - 1}">&laquo;</button>`;

    const start = Math.max(1, currentPage - 3);
    const end = Math.min(totalPages, currentPage + 3);

    if (start > 1) html += `<button data-page="1">1</button><span>...</span>`;
    for (let i = start; i <= end; i++) {
      html += `<button class="${i === currentPage ? 'active' : ''}" data-page="${i}">${i}</button>`;
    }
    if (end < totalPages) html += `<span>...</span><button data-page="${totalPages}">${totalPages}</button>`;

    html += `<button ${currentPage === totalPages ? 'disabled' : ''} data-page="${currentPage + 1}">&raquo;</button>`;

    pag.innerHTML = html;
    pag.querySelectorAll('button').forEach(btn => {
      btn.addEventListener('click', () => {
        currentPage = +btn.dataset.page;
        renderTable();
        document.getElementById('crimes-table-wrapper').scrollIntoView({ behavior: 'smooth' });
      });
    });
  }

  // ─── Dosimetria ──────────────────────────────────────────────────────────
  function calcDosimetria() {
    if (!selectedCrime) {
      document.getElementById('resultado-dosimetria').innerHTML = '<em>Selecione um crime acima</em>';
      return;
    }

    const penaMin = selectedCrime.pena_min;
    const penaMax = selectedCrime.pena_max;
    const intervalo = penaMax - penaMin;

    // 1st phase: each unfavorable circumstance adds 1/8 of the interval
    const circDesfav = document.querySelectorAll('.circ-judicial:checked').length;
    const penaBase = penaMin + (intervalo * circDesfav / 8);

    document.getElementById('pena-base-result').textContent = formatPena(Math.round(penaBase));

    // 2nd phase: agravantes/atenuantes (1/6 each, cannot exceed limits)
    const agravantes = +document.getElementById('agravantes').value || 0;
    const atenuantes = +document.getElementById('atenuantes').value || 0;
    const fracao2 = 1 / 6;
    let penaInter = penaBase + (penaBase * fracao2 * agravantes) - (penaBase * fracao2 * atenuantes);
    penaInter = Math.max(penaMin, Math.min(penaMax, penaInter));

    document.getElementById('pena-inter-result').textContent = formatPena(Math.round(penaInter));

    // 3rd phase: increases/decreases (can exceed limits)
    const aumento = +document.getElementById('aumento').value || 0;
    const diminuicao = +document.getElementById('diminuicao').value || 0;
    let penaDef = penaInter + (penaInter * aumento) - (penaInter * diminuicao);
    penaDef = Math.max(1, penaDef);

    document.getElementById('pena-def-result').textContent = formatPena(Math.round(penaDef));

    // Result
    const anos = Math.floor(penaDef / 12);
    const meses = Math.round(penaDef % 12);
    const regime = penaDef > 96 ? 'Fechado' : penaDef > 48 ? 'Semiaberto' : 'Aberto';
    const substituicao = penaDef <= 48 && selectedCrime.violencia !== 'Sim' && selectedCrime.grave_ameaca !== 'Sim';

    document.getElementById('resultado-dosimetria').innerHTML = `
      <strong>Pena definitiva: ${anos} ano(s) e ${meses} mes(es) de ${selectedCrime.tipo_pena}</strong><br>
      Regime inicial: <strong>${regime}</strong> (Art. 33, §2º CP)<br>
      ${selectedCrime.hediondo === 'Sim' ? '<span class="badge badge-hediondo">Crime Hediondo</span> — Regime inicial fechado obrigatório (Art. 2º, §1º, Lei 8.072/90)<br>' : ''}
      ${substituicao ? 'Cabe substituição por pena restritiva de direitos (Art. 44 CP)<br>' : ''}
      ${penaDef <= 24 ? 'Cabe <em>sursis</em> da pena (Art. 77 CP)<br>' : ''}
      ${penaMin <= 48 && selectedCrime.violencia !== 'Sim' ? 'Pode caber ANPP (Art. 28-A CPP) — pena mínima inferior a 4 anos<br>' : ''}
    `;
  }

  // ─── Statistics ──────────────────────────────────────────────────────────
  function renderStats() {
    const total = crimes.length;
    const leis = [...new Set(crimes.map(c => c.lei))];
    const hediondos = crimes.filter(c => c.hediondo === 'Sim').length;
    const violencia = crimes.filter(c => c.violencia === 'Sim').length;
    const graveAmeaca = crimes.filter(c => c.grave_ameaca === 'Sim').length;
    const dolosos = crimes.filter(c => c.elemento === 'Doloso').length;
    const culposos = crimes.filter(c => c.elemento === 'Culposo').length;
    const reclusao = crimes.filter(c => c.tipo_pena === 'Reclusão').length;

    const statsGrid = document.getElementById('stats-grid');
    statsGrid.innerHTML = [
      { n: total, l: 'Tipos Penais' },
      { n: leis.length, l: 'Diplomas Legislativos' },
      { n: hediondos, l: 'Hediondos' },
      { n: violencia, l: 'Com Violência' },
      { n: graveAmeaca, l: 'Com Grave Ameaça' },
      { n: dolosos, l: 'Dolosos' },
      { n: culposos, l: 'Culposos' },
      { n: reclusao, l: 'Reclusão' },
    ].map(s => `<div class="stat-card"><div class="stat-number">${s.n}</div><div class="stat-label">${s.l}</div></div>`).join('');

    // Per-law distribution
    const perLei = {};
    crimes.forEach(c => { perLei[c.lei] = (perLei[c.lei] || 0) + 1; });
    const sorted = Object.entries(perLei).sort((a, b) => b[1] - a[1]);

    document.getElementById('stats-leis').innerHTML = sorted.map(([lei, count]) =>
      `<div class="lei-item"><span class="lei-name">${lei}</span><span class="lei-count">${count}</span></div>`
    ).join('');
  }

  // ─── Utils ───────────────────────────────────────────────────────────────
  function formatPena(meses) {
    if (!meses && meses !== 0) return '—';
    if (meses === 0) return '—';
    const anos = Math.floor(meses / 12);
    const m = meses % 12;
    if (anos === 0) return `${m}m`;
    if (m === 0) return `${anos}a`;
    return `${anos}a${m}m`;
  }

  // ─── Start ───────────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', init);
})();

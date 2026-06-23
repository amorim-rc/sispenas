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
    bindProgressao();
    bindPrescricao();
    bindConcurso();
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

  // ─── Progressão ─────────────────────────────────────────────────────────
  function bindProgressao() {
    document.getElementById('btn-calc-progressao').addEventListener('click', calcProgressao);
  }

  function calcProgressao() {
    const penaTotal = +document.getElementById('prog-pena-total').value;
    const tempoCumprido = +document.getElementById('prog-tempo-cumprido').value;
    const regimeAtual = document.getElementById('prog-regime-atual').value;
    const classificacao = document.getElementById('prog-classificacao').value;
    const primario = document.getElementById('prog-primario').checked;
    const bomComportamento = document.getElementById('prog-bom-comportamento').checked;

    // Frações do Art. 112 LEP (Lei 13.964/2019 - Pacote Anticrime)
    const fracoes = {
      'comum': primario ? 1/6 : 1/6,
      'hediondo-primario': 2/5,
      'hediondo-reincidente': 3/5,
      'hediondo-reincidente-especifico': 7/10,
      'comando-org-criminosa': 1/2,
      'milicia': 1/2
    };

    // Frações específicas por regime (Art. 112 LEP atualizado)
    let fracao;
    if (classificacao === 'comum') {
      fracao = primario ? 1/6 : 1/6; // 16% comum
    } else if (classificacao === 'hediondo-primario') {
      fracao = 2/5; // 40%
    } else if (classificacao === 'hediondo-reincidente') {
      fracao = 3/5; // 60%
    } else if (classificacao === 'hediondo-reincidente-especifico') {
      fracao = 7/10; // 70% (com resultado morte, vedada progressão ao aberto em algumas hipóteses)
    } else {
      fracao = 1/2; // 50% para comandante de org. criminosa e milícia
    }

    const tempoNecessario = Math.ceil(penaTotal * fracao);
    const tempoRestante = Math.max(0, tempoNecessario - tempoCumprido);

    // Livramento condicional (Art. 83 CP)
    let fracaoLivramento;
    if (classificacao.startsWith('hediondo')) {
      fracaoLivramento = primario ? 2/3 : null; // Reincidente específico: vedado
    } else {
      fracaoLivramento = primario ? 1/3 : 1/2;
    }

    const tempoLivramento = fracaoLivramento ? Math.ceil(penaTotal * fracaoLivramento) : null;
    const restanteLivramento = tempoLivramento ? Math.max(0, tempoLivramento - tempoCumprido) : null;

    // Regime progressão destino
    const proximoRegime = regimeAtual === 'fechado' ? 'Semiaberto' :
                          regimeAtual === 'semiaberto' ? 'Aberto' : '—';

    const resultado = document.getElementById('resultado-progressao');
    resultado.innerHTML = `
      <strong>Fração aplicável:</strong> ${formatFracao(fracao)} (${(fracao * 100).toFixed(1)}%)<br>
      <strong>Tempo necessário:</strong> ${formatPena(tempoNecessario)}<br>
      <strong>Tempo já cumprido:</strong> ${formatPena(tempoCumprido)}<br>
      <strong>Tempo restante:</strong> ${tempoRestante > 0 ? formatPena(tempoRestante) : 'Já cumpriu!'}<br>
      <strong>Próximo regime:</strong> ${proximoRegime}<br>
      ${!bomComportamento ? '<br><em>Atenção: Bom comportamento carcerário é requisito subjetivo (Art. 112, §1º LEP)</em>' : ''}
      ${classificacao.startsWith('hediondo') ? '<br><em>Crime hediondo: regime inicial fechado (Art. 2º, §1º, Lei 8.072/90)</em>' : ''}
    `;

    // Livramento
    const resLivramento = document.getElementById('resultado-livramento');
    if (fracaoLivramento === null) {
      resLivramento.innerHTML = '<strong>Vedado</strong> — Reincidente específico em crime hediondo (Art. 83, V, CP)';
    } else {
      resLivramento.innerHTML = `
        <strong>Fração:</strong> ${formatFracao(fracaoLivramento)} (${(fracaoLivramento * 100).toFixed(1)}%)<br>
        <strong>Tempo necessário:</strong> ${formatPena(tempoLivramento)}<br>
        <strong>Tempo restante:</strong> ${restanteLivramento > 0 ? formatPena(restanteLivramento) : 'Já cumpriu!'}<br>
        <em>Requisitos adicionais: bom comportamento, aptidão para trabalho, reparação do dano (Art. 83 CP)</em>
      `;
    }
  }

  function formatFracao(f) {
    const map = { '0.167': '1/6', '0.25': '1/4', '0.333': '1/3', '0.4': '2/5', '0.5': '1/2', '0.6': '3/5', '0.667': '2/3', '0.7': '7/10' };
    const key = f.toFixed(3);
    return map[key] || f.toFixed(3);
  }

  // ─── Prescrição ─────────────────────────────────────────────────────────
  function bindPrescricao() {
    document.getElementById('btn-calc-prescricao').addEventListener('click', calcPrescricao);
  }

  function calcPrescricao() {
    const penaMax = +document.getElementById('presc-pena-max').value;
    const penaConcreta = +document.getElementById('presc-pena-concreta').value;
    const idadeFato = +document.getElementById('presc-idade-fato').value;
    const idadeSentenca = +document.getElementById('presc-idade-sentenca').value;
    const reincidente = document.getElementById('presc-reincidente').checked;
    const tipo = document.getElementById('presc-tipo').value;

    // Tabela Art. 109 CP (pena em meses → prazo prescricional em meses)
    function prazoPrescricional(penaMeses) {
      if (penaMeses > 144) return 240;      // > 12 anos → 20 anos
      if (penaMeses > 96) return 192;        // > 8 anos → 16 anos
      if (penaMeses > 48) return 144;        // > 4 anos → 12 anos
      if (penaMeses > 24) return 96;         // > 2 anos → 8 anos
      if (penaMeses >= 12) return 48;        // >= 1 ano → 4 anos
      return 36;                             // < 1 ano → 3 anos
    }

    let penaReferencia;
    if (tipo === 'abstrata') {
      penaReferencia = penaMax;
    } else {
      penaReferencia = penaConcreta || penaMax;
    }

    let prazo = prazoPrescricional(penaReferencia);

    // Redução pela metade para menor de 21 na data do fato ou maior de 70 na sentença (Art. 115 CP)
    let reducao = false;
    if (idadeFato < 21 || idadeSentenca >= 70) {
      prazo = Math.floor(prazo / 2);
      reducao = true;
    }

    // Aumento de 1/3 para reincidente (somente prescrição executória, Art. 110 CP)
    let aumentoReinc = false;
    if (reincidente && tipo === 'executoria') {
      prazo = Math.ceil(prazo * 4 / 3);
      aumentoReinc = true;
    }

    const resultado = document.getElementById('resultado-prescricao');
    resultado.innerHTML = `
      <strong>Tipo:</strong> ${tipo === 'abstrata' ? 'Prescrição da pretensão punitiva (em abstrato)' :
                              tipo === 'retroativa' ? 'Prescrição retroativa (pena concreta)' :
                              'Prescrição da pretensão executória'}<br>
      <strong>Pena de referência:</strong> ${formatPena(penaReferencia)}<br>
      <strong>Prazo prescricional:</strong> ${formatPena(prazo)} (${Math.floor(prazo/12)} anos${prazo%12 ? ' e ' + prazo%12 + ' meses' : ''})<br>
      ${reducao ? '<br><em>Redução de 1/2 aplicada (Art. 115 CP — menor de 21 na data do fato ou maior de 70 na sentença)</em>' : ''}
      ${aumentoReinc ? '<br><em>Aumento de 1/3 aplicado (reincidência — prescrição executória)</em>' : ''}
      <br><br>
      <strong>Marcos interruptivos (Art. 117 CP):</strong><br>
      I — Recebimento da denúncia/queixa<br>
      II — Pronúncia (crimes dolosos contra a vida)<br>
      III — Decisão confirmatória da pronúncia<br>
      IV — Publicação da sentença/acórdão condenatório recorrível<br>
      V — Início/continuação do cumprimento da pena<br>
      VI — Reincidência
    `;
  }

  // ─── Concurso ───────────────────────────────────────────────────────────
  function bindConcurso() {
    document.getElementById('btn-calc-concurso').addEventListener('click', calcConcurso);
    document.getElementById('btn-add-crime').addEventListener('click', () => {
      const list = document.getElementById('conc-penas-list');
      const count = list.children.length + 1;
      const row = document.createElement('div');
      row.className = 'conc-pena-row';
      row.innerHTML = `<input type="number" class="conc-pena-input" min="1" max="1200" value="12" placeholder="Pena em meses"><span class="conc-pena-label">Crime ${count}</span>`;
      list.appendChild(row);
      document.getElementById('conc-num-crimes').value = count;
    });
    document.getElementById('btn-remove-crime').addEventListener('click', () => {
      const list = document.getElementById('conc-penas-list');
      if (list.children.length > 2) {
        list.removeChild(list.lastChild);
        document.getElementById('conc-num-crimes').value = list.children.length;
      }
    });
  }

  function calcConcurso() {
    const tipo = document.getElementById('conc-tipo').value;
    const inputs = document.querySelectorAll('.conc-pena-input');
    const penas = Array.from(inputs).map(i => +i.value).filter(v => v > 0);
    const fracao = +document.getElementById('conc-fracao').value;

    if (penas.length < 2) {
      document.getElementById('resultado-concurso').innerHTML = '<em>Informe ao menos 2 crimes</em>';
      return;
    }

    const soma = penas.reduce((a, b) => a + b, 0);
    const maior = Math.max(...penas);
    let resultado, metodo, penafinal;

    switch (tipo) {
      case 'material':
      case 'formal-improprio':
        penafinal = soma;
        metodo = 'Cúmulo material — soma das penas';
        break;
      case 'formal-proprio':
        penafinal = maior + Math.ceil(maior * fracao);
        metodo = `Exasperação — maior pena (${formatPena(maior)}) + fração de ${(fracao * 100).toFixed(1)}%`;
        break;
      case 'continuado':
        penafinal = maior + Math.ceil(maior * fracao);
        metodo = `Exasperação — maior pena (${formatPena(maior)}) + fração de ${(fracao * 100).toFixed(1)}%`;
        break;
      case 'continuado-especifico':
        penafinal = maior + Math.ceil(maior * fracao);
        metodo = `Exasperação — maior pena (${formatPena(maior)}) × fração (máx. triplo)`;
        break;
    }

    // Concurso formal: se exasperação > soma, aplica cúmulo (Art. 70, §único)
    let concursoBeneficio = '';
    if ((tipo === 'formal-proprio' || tipo === 'continuado') && penafinal > soma) {
      concursoBeneficio = `<br><em>Atenção: resultado da exasperação (${formatPena(penafinal)}) supera o cúmulo material (${formatPena(soma)}). Aplica-se o cúmulo material como limite (Art. 70, §único CP).</em>`;
      penafinal = soma;
    }

    const regimeFinal = penafinal > 96 ? 'Fechado' : penafinal > 48 ? 'Semiaberto' : 'Aberto';

    document.getElementById('resultado-concurso').innerHTML = `
      <strong>Método:</strong> ${metodo}<br>
      <strong>Penas individuais:</strong> ${penas.map(p => formatPena(p)).join(' + ')} = ${formatPena(soma)}<br>
      <strong>Pena final do concurso:</strong> ${formatPena(penafinal)}<br>
      <strong>Regime inicial:</strong> ${regimeFinal}<br>
      ${concursoBeneficio}
      <br><br>
      <strong>Referência:</strong><br>
      Art. 69 — Concurso material: soma das penas<br>
      Art. 70 — Concurso formal próprio: maior pena + 1/6 a 1/2<br>
      Art. 70, 2ª parte — Formal impróprio: soma (desígnios autônomos)<br>
      Art. 71 — Continuado: maior pena + 1/6 a 2/3<br>
      Art. 71, §único — Continuado específico (vítimas diferentes, violência): até o triplo
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

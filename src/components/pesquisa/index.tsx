import React, {useCallback, useEffect, useMemo, useState} from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import {useCrimes} from '@site/src/lib/useCrimes';
import type {Crime, PenaPrivativa} from '@site/src/lib/types';
import Detalhe from './Detalhe';
import styles from './styles.module.css';

const PAGE_SIZE = 40;
const MODALIDADES: {key: string; label: string}[] = [
  {key: 'Reclusão', label: 'Reclusão'},
  {key: 'Detenção', label: 'Detenção'},
  {key: 'Prisão simples', label: 'Prisão simples'},
  {key: 'Multa', label: 'Multa'},
];

interface Filtros {
  q: string;
  lei: string;
  modalidades: Set<string>;
  hediondo: string;
  elemento: string;
  violencia: string;
  acao: string;
  menorPotencial: boolean;
}

function initialFiltros(): Filtros {
  return {q: '', lei: '', modalidades: new Set(), hediondo: '', elemento: '', violencia: '', acao: '', menorPotencial: false};
}

function matches(c: Crime, f: Filtros): boolean {
  if (f.q) {
    const q = f.q.toLowerCase();
    const hit =
      c.crime.toLowerCase().includes(q) ||
      c.artigo.toLowerCase().includes(q) ||
      c.lei.toLowerCase().includes(q) ||
      (c.obs || '').toLowerCase().includes(q);
    if (!hit) return false;
  }
  if (f.lei && c.lei !== f.lei) return false;

  if (f.modalidades.size > 0) {
    const privSel = [...f.modalidades].filter((m) => m !== 'Multa');
    const multaSel = f.modalidades.has('Multa');
    // Privativas: OR entre as selecionadas (uma que corresponda basta).
    if (privSel.length > 0 && !privSel.includes(c.pena_privativa)) return false;
    // Multa: filtro AND (exige multa quando marcada).
    if (multaSel && !c.tem_multa) return false;
  }

  if (f.hediondo && c.hediondo !== f.hediondo) return false;
  if (f.elemento && c.elemento !== f.elemento) return false;
  if (f.violencia === 'violencia' && c.violencia !== 'Sim') return false;
  if (f.violencia === 'grave_ameaca' && c.grave_ameaca !== 'Sim') return false;
  if (f.violencia === 'ambos' && !(c.violencia === 'Sim' && c.grave_ameaca === 'Sim')) return false;
  if (f.violencia === 'nenhuma' && (c.violencia === 'Sim' || c.grave_ameaca === 'Sim')) return false;
  if (f.acao && c.acao !== f.acao) return false;
  if (f.menorPotencial && !c.infracao_menor_potencial) return false;
  return true;
}

type SortField = 'lei' | 'artigo' | 'crime' | 'pena_min_meses' | 'pena_max_meses';

function PesquisaInner() {
  const {crimes, loading, error} = useCrimes();
  const [f, setF] = useState<Filtros>(initialFiltros);
  const [sortField, setSortField] = useState<SortField>('lei');
  const [sortAsc, setSortAsc] = useState(true);
  const [page, setPage] = useState(1);
  const [selectedId, setSelectedId] = useState<number | null>(() => {
    if (typeof window === 'undefined') return null;
    const t = new URLSearchParams(window.location.search).get('tipo');
    return t ? Number(t) : null;
  });

  const selectCrime = useCallback((id: number | null) => {
    setSelectedId(id);
    const url = new URL(window.location.href);
    if (id === null) url.searchParams.delete('tipo');
    else url.searchParams.set('tipo', String(id));
    window.history.pushState({tipo: id}, '', url.toString());
    window.scrollTo({top: 0, behavior: 'auto'});
  }, []);

  useEffect(() => {
    const sync = () => {
      const t = new URLSearchParams(window.location.search).get('tipo');
      setSelectedId(t ? Number(t) : null);
    };
    window.addEventListener('popstate', sync);
    return () => window.removeEventListener('popstate', sync);
  }, []);

  const leis = useMemo(() => [...new Set(crimes.map((c) => c.lei))].sort(), [crimes]);
  const acoes = useMemo(() => [...new Set(crimes.map((c) => c.acao))].filter((a) => a && a !== '—').sort(), [crimes]);

  const filtered = useMemo(() => crimes.filter((c) => matches(c, f)), [crimes, f]);

  const sorted = useMemo(() => {
    const arr = [...filtered];
    arr.sort((a, b) => {
      const va = a[sortField];
      const vb = b[sortField];
      let cmp: number;
      if (typeof va === 'number' && typeof vb === 'number') cmp = va - vb;
      else cmp = String(va).localeCompare(String(vb), 'pt-BR');
      return sortAsc ? cmp : -cmp;
    });
    return arr;
  }, [filtered, sortField, sortAsc]);

  const totalPages = Math.max(1, Math.ceil(sorted.length / PAGE_SIZE));
  const pageClamped = Math.min(page, totalPages);
  const pageItems = sorted.slice((pageClamped - 1) * PAGE_SIZE, pageClamped * PAGE_SIZE);
  const selected = crimes.find((c) => c.id === selectedId) || null;

  const update = (patch: Partial<Filtros>) => {
    setF((prev) => ({...prev, ...patch}));
    setPage(1);
  };

  const toggleModalidade = (key: string) => {
    setF((prev) => {
      const next = new Set(prev.modalidades);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return {...prev, modalidades: next};
    });
    setPage(1);
  };

  const sortBy = (field: SortField) => {
    if (field === sortField) setSortAsc((s) => !s);
    else {
      setSortField(field);
      setSortAsc(true);
    }
  };

  if (loading) return <div className={styles.loading}>Carregando catálogo de tipos penais…</div>;
  if (error) return <div className={styles.error}>Erro ao carregar os dados: {error}</div>;

  if (selected) {
    return (
      <div className={styles.wrap}>
        <button className={styles.voltarBtn} onClick={() => selectCrime(null)}>
          ← Voltar à pesquisa
        </button>
        <Detalhe crime={selected} todos={crimes} onSelect={selectCrime} />
      </div>
    );
  }

  return (
    <div className={styles.wrap}>
      <div className={styles.searchBar}>
        <input
          className={styles.search}
          type="text"
          placeholder="Buscar por crime, artigo, lei ou benefício…"
          value={f.q}
          onChange={(e) => update({q: e.target.value})}
        />
        <span className={styles.count}>{filtered.length} de {crimes.length} tipos</span>
      </div>

      <div className={styles.filtros}>
        <select value={f.lei} onChange={(e) => update({lei: e.target.value})}>
          <option value="">Todas as leis</option>
          {leis.map((l) => <option key={l} value={l}>{l}</option>)}
        </select>
        <select value={f.hediondo} onChange={(e) => update({hediondo: e.target.value})}>
          <option value="">Hediondo?</option>
          <option value="Sim">Hediondo</option>
          <option value="Não">Não hediondo</option>
        </select>
        <select value={f.elemento} onChange={(e) => update({elemento: e.target.value})}>
          <option value="">Elemento subjetivo</option>
          <option value="Doloso">Doloso</option>
          <option value="Culposo">Culposo</option>
          <option value="Preterdoloso">Preterdoloso</option>
        </select>
        <select value={f.violencia} onChange={(e) => update({violencia: e.target.value})}>
          <option value="">Violência/ameaça</option>
          <option value="violencia">Com violência</option>
          <option value="grave_ameaca">Com grave ameaça</option>
          <option value="ambos">Ambos</option>
          <option value="nenhuma">Sem violência/ameaça</option>
        </select>
        <select value={f.acao} onChange={(e) => update({acao: e.target.value})}>
          <option value="">Ação penal</option>
          {acoes.map((a) => <option key={a} value={a}>{a}</option>)}
        </select>
        <label className={styles.chkInline}>
          <input type="checkbox" checked={f.menorPotencial} onChange={(e) => update({menorPotencial: e.target.checked})} />
          Menor potencial ofensivo
        </label>
        <button className={styles.clearBtn} onClick={() => { setF(initialFiltros()); setPage(1); }}>
          Limpar filtros
        </button>
      </div>

      <div className={styles.modalidades}>
        <span className={styles.modLabel}>Modalidade de pena:</span>
        {MODALIDADES.map((m) => (
          <button
            key={m.key}
            className={`${styles.modChip} ${f.modalidades.has(m.key) ? styles.modChipOn : ''}`}
            onClick={() => toggleModalidade(m.key)}
          >
            {m.label}
          </button>
        ))}
        <span className={styles.modDica}>Selecionar "Reclusão" inclui reclusão + multa. Combine com "Multa" para restringir.</span>
      </div>

      <div className={styles.tableWrap}>
        <table className={styles.table}>
          <thead>
            <tr>
              {([['lei', 'Lei'], ['artigo', 'Artigo'], ['crime', 'Crime'], ['pena_min_meses', 'Pena mín.'], ['pena_max_meses', 'Pena máx.']] as [SortField, string][]).map(([field, label]) => (
                <th key={field} className={styles.sortable} onClick={() => sortBy(field)}>
                  {label}{sortField === field ? (sortAsc ? ' ▲' : ' ▼') : ''}
                </th>
              ))}
              <th>Modalidade</th>
            </tr>
          </thead>
          <tbody>
            {pageItems.map((c) => {
              const rowCls = c.hediondo === 'Sim' ? styles.rowHed : (c.violencia === 'Sim' || c.grave_ameaca === 'Sim') ? styles.rowViol : '';
              return (
                <tr key={c.id} className={rowCls} onClick={() => selectCrime(c.id)}>
                  <td>{c.lei}</td>
                  <td>{c.artigo}</td>
                  <td>{c.crime}</td>
                  <td className={styles.penaCell}>{c.pena_min_rotulo}</td>
                  <td className={styles.penaCell}>{c.pena_max_rotulo}</td>
                  <td>
                    <span className={styles.modTag}>{c.pena_privativa === 'Nenhuma' ? '—' : c.pena_privativa}</span>
                    {c.tem_multa && <span className={styles.modTagMulta}>+ multa</span>}
                    {c.hediondo === 'Sim' && <span className={styles.modTagHed}>H</span>}
                  </td>
                </tr>
              );
            })}
            {pageItems.length === 0 && (
              <tr><td colSpan={6} className={styles.vazio}>Nenhum tipo penal encontrado com esses filtros.</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className={styles.pagination}>
          <button disabled={pageClamped === 1} onClick={() => setPage(pageClamped - 1)}>«</button>
          <span>Página {pageClamped} de {totalPages}</span>
          <button disabled={pageClamped === totalPages} onClick={() => setPage(pageClamped + 1)}>»</button>
        </div>
      )}

      <div className={styles.placeholder}>
        Selecione um tipo penal na tabela para abrir a página do tipo com o cálculo dinâmico dos benefícios penais aplicáveis.
      </div>
    </div>
  );
}

export default function Pesquisa() {
  return <BrowserOnly fallback={<div className={styles.loading}>Carregando…</div>}>{() => <PesquisaInner />}</BrowserOnly>;
}

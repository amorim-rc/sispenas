// Concurso de crimes (arts. 69-71) — combinador de molduras já definitivas.
//
// Diferente dos modificadores das três fases, o concurso não desloca a pena de
// UM tipo: ele combina as penas de VÁRIOS. Por isso tem seção própria, e opera
// sobre penas que já passaram pela dosimetria.
//
// A modalidade é de escolha ÚNICA e desmarcável: escolhida, a pena cumulada
// substitui a pena concreta que alimenta os benefícios — porque é ela, e não a
// pena do tipo isolado, que define o que o réu tem direito a pleitear.

import React, {useEffect, useMemo, useState} from 'react';

import type {Crime} from '@site/src/lib/types';
import {calcularConcurso} from '@site/src/lib/dosimetria';

import styles from './styles.module.css';

function meses(v: number): string {
  const anos = Math.floor(v / 12);
  const m = Math.round((v - anos * 12) * 10) / 10;
  if (anos && m) return `${anos}a ${m}m`;
  if (anos) return `${anos} ano${anos > 1 ? 's' : ''}`;
  return `${m} m${m === 1 ? 'ês' : 'eses'}`;
}

/** "Art. 64 · CDC (Lei 8.078/90)" — identifica o dispositivo, não o repete. */
function referencia(c: Crime): string {
  return `${c.artigo} · ${c.lei.replace(/\s*\(atualiz\.\)/, '')}`;
}

type Linha = {
  chave: string;
  titulo: string;
  total: number;
  dispositivo: string;
  memoria: string;
};

export default function Concurso({
  crime,
  penaAtual,
  todos,
  onPenaConcurso,
}: {
  crime: Crime;
  /** Pena definitiva do tipo em foco (resultado da dosimetria). */
  penaAtual: number;
  todos: Crime[];
  /** Pena cumulada da modalidade escolhida, ou null quando nenhuma está. */
  onPenaConcurso: (v: number | null) => void;
}) {
  const [outros, setOutros] = useState<Crime[]>([]);
  const [busca, setBusca] = useState('');
  const [escolhida, setEscolhida] = useState<string | null>(null);

  const candidatos = useMemo(() => {
    const termo = busca.trim().toLowerCase();
    if (termo.length < 2) return [];
    return todos
      .filter((c) => c.id !== crime.id && !outros.some((o) => o.id === c.id))
      .filter((c) => c.tem_pena_privativa !== false)
      .filter(
        (c) =>
          c.crime.toLowerCase().includes(termo) ||
          c.artigo.toLowerCase().includes(termo) ||
          c.lei.toLowerCase().includes(termo),
      )
      .slice(0, 8);
  }, [busca, todos, crime.id, outros]);

  // Presume-se cada crime adicionado condenado no mínimo — a mesma convenção
  // da busca por benefício, e a hipótese mais favorável ao réu.
  const penas = [penaAtual, ...outros.map((o) => o.pena_min_meses || o.pena_max_meses)];

  const modalidades: Linha[] = useMemo(() => {
    if (penas.length < 2) return [];
    const r = (
      chave: string,
      titulo: string,
      m: 'material' | 'formal' | 'continuado',
      f?: number,
    ): Linha => ({chave, titulo, ...calcularConcurso(penas, m, f)});
    return [
      r('material', 'Material (soma)', 'material'),
      r('formal-min', 'Formal · +1/6', 'formal', 1 / 6),
      r('formal-max', 'Formal · +1/2', 'formal', 1 / 2),
      r('cont-min', 'Continuado · +1/6', 'continuado', 1 / 6),
      r('cont-max', 'Continuado · +2/3', 'continuado', 2 / 3),
    ];
  }, [penas.join(',')]);

  const maisFavoravel = modalidades.length
    ? Math.min(...modalidades.map((m) => m.total))
    : 0;

  // Sem crimes acrescentados não há concurso: a escolha cai e os benefícios
  // voltam à pena do tipo isolado.
  useEffect(() => {
    if (modalidades.length === 0 && escolhida !== null) setEscolhida(null);
  }, [modalidades.length]);

  const selecionada = modalidades.find((m) => m.chave === escolhida) ?? null;

  useEffect(() => {
    onPenaConcurso(selecionada ? selecionada.total : null);
  }, [selecionada?.chave, selecionada?.total]);

  if (!crime.tem_pena_privativa) return null;

  return (
    <div className={styles.concurso}>
      <h4 className={styles.benefSecTitulo}>Concurso de crimes — arts. 69 a 71</h4>
      <p className={styles.simDica}>
        Acrescente outros crimes e escolha a modalidade. A pena cumulada da modalidade
        marcada passa a alimentar os benefícios. Os crimes acrescentados são presumidos
        no mínimo cominado; a pena deste tipo vem da dosimetria acima.
      </p>

      <div className={styles.concursoLista}>
        <span className={`${styles.concursoChip} ${styles.concursoChipFoco}`}>
          <span className={styles.chipRef}>{referencia(crime)}</span>
          <span className={styles.chipNome}>{crime.crime}</span>
          <span className={styles.chipPena}>Pena de {meses(penaAtual)}</span>
        </span>
        {outros.map((o) => (
          <span key={o.id} className={styles.concursoChip}>
            <span className={styles.chipRef}>{referencia(o)}</span>
            <span className={styles.chipNome}>{o.crime}</span>
            <span className={styles.chipPena}>
              Pena de {meses(o.pena_min_meses || o.pena_max_meses)}
            </span>
            <button
              type="button"
              className={styles.chipRemover}
              aria-label={`Remover ${o.crime}`}
              onClick={() => setOutros((p) => p.filter((x) => x.id !== o.id))}>
              ×
            </button>
          </span>
        ))}
      </div>

      <div className={styles.concursoBusca}>
        <input
          type="search"
          placeholder="Acrescentar outro crime (nome, artigo ou lei)…"
          value={busca}
          onChange={(e) => setBusca(e.target.value)}
        />
        {candidatos.length > 0 && (
          <ul className={styles.concursoSugestoes}>
            {candidatos.map((c) => (
              <li key={c.id}>
                <button
                  type="button"
                  onClick={() => {
                    setOutros((p) => [...p, c]);
                    setBusca('');
                  }}>
                  <strong>{c.crime}</strong>
                  <span>{referencia(c)}</span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      {modalidades.length === 0 ? (
        <p className={styles.faseVazia}>
          Acrescente ao menos um crime para comparar as modalidades.
        </p>
      ) : (
        <ul className={styles.concursoOpcoes}>
          {modalidades.map((m) => (
            <li key={m.chave}>
              <label
                className={[
                  styles.concursoOpcao,
                  m.total === maisFavoravel ? styles.concursoFavoravel : '',
                  escolhida === m.chave ? styles.concursoAtiva : '',
                ].join(' ')}
                title={m.memoria}>
                <input
                  type="checkbox"
                  checked={escolhida === m.chave}
                  // Marca única, porém desmarcável: um réu é condenado por uma
                  // modalidade só, mas o usuário precisa poder voltar atrás.
                  onChange={() =>
                    setEscolhida((p) => (p === m.chave ? null : m.chave))
                  }
                />
                <span className={styles.concursoOpcaoNome}>
                  {m.titulo}
                  <em>{m.dispositivo}</em>
                </span>
                <strong className={styles.concursoTotal}>{meses(m.total)}</strong>
              </label>
            </li>
          ))}
        </ul>
      )}

      {modalidades.length > 0 && (
        <p className={styles.concursoNota}>
          {selecionada ? (
            <>
              Aplicando <strong>{selecionada.titulo}</strong>: pena cumulada de{' '}
              <strong>{meses(selecionada.total)}</strong>. {selecionada.memoria}
            </>
          ) : (
            <>
              Em destaque, o resultado <strong>mais favorável ao réu</strong> (
              {meses(maisFavoravel)}). Pelo art. 70, parágrafo único, a exasperação
              nunca supera a soma do cúmulo material.
            </>
          )}
        </p>
      )}
    </div>
  );
}

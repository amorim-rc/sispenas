// Concurso de crimes (arts. 69-71) — combinador de molduras já definitivas.
//
// Diferente dos modificadores das três fases, o concurso não desloca a pena de
// UM tipo: ele combina as penas de VÁRIOS. Por isso tem seção própria, e opera
// sobre penas que já passaram pela dosimetria.

import React, {useMemo, useState} from 'react';

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

export default function Concurso({
  crime,
  penaAtual,
  todos,
}: {
  crime: Crime;
  /** Pena definitiva do tipo em foco (resultado da dosimetria). */
  penaAtual: number;
  todos: Crime[];
}) {
  const [outros, setOutros] = useState<Crime[]>([]);
  const [busca, setBusca] = useState('');

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

  const modalidades = useMemo(() => {
    if (penas.length < 2) return [];
    return [
      {...calcularConcurso(penas, 'material'), chave: 'material'},
      {...calcularConcurso(penas, 'formal', 1 / 6), chave: 'formal-min'},
      {...calcularConcurso(penas, 'formal', 1 / 2), chave: 'formal-max'},
      {...calcularConcurso(penas, 'continuado', 1 / 6), chave: 'cont-min'},
      {...calcularConcurso(penas, 'continuado', 2 / 3), chave: 'cont-max'},
    ];
  }, [penas.join(',')]);

  const maisFavoravel = modalidades.length
    ? Math.min(...modalidades.map((m) => m.total))
    : 0;

  if (!crime.tem_pena_privativa) return null;

  return (
    <div className={styles.concurso}>
      <h4 className={styles.benefSecTitulo}>Concurso de crimes — arts. 69 a 71</h4>
      <p className={styles.simDica}>
        Combine este tipo com outros para comparar as modalidades de concurso. As penas
        dos crimes acrescentados são presumidas no mínimo cominado; a deste tipo vem da
        dosimetria acima.
      </p>

      <div className={styles.concursoLista}>
        <span className={styles.concursoChip}>
          <strong>{crime.crime}</strong>
          <em>{meses(penaAtual)}</em>
        </span>
        {outros.map((o) => (
          <span key={o.id} className={styles.concursoChip}>
            <strong>{o.crime}</strong>
            <em>{meses(o.pena_min_meses || o.pena_max_meses)}</em>
            <button
              type="button"
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
                  <span>{c.lei} · {c.artigo} · {c.pena_faixa_rotulo}</span>
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
        <table className={styles.concursoTabela}>
          <thead>
            <tr>
              <th>Modalidade</th>
              <th>Total</th>
              <th>Como se chega</th>
            </tr>
          </thead>
          <tbody>
            {modalidades.map((m) => (
              <tr
                key={m.chave}
                className={m.total === maisFavoravel ? styles.concursoFavoravel : ''}>
                <td>
                  {m.modalidade}
                  <span className={styles.concursoDisp}>{m.dispositivo}</span>
                </td>
                <td className={styles.concursoTotal}>{meses(m.total)}</td>
                <td className={styles.concursoMemoria}>{m.memoria}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {modalidades.length > 0 && (
        <p className={styles.concursoNota}>
          Destacado, o resultado <strong>mais favorável ao réu</strong> ({meses(maisFavoravel)}).
          Pelo art. 70, parágrafo único, a exasperação nunca pode superar a soma do cúmulo
          material.
        </p>
      )}
    </div>
  );
}

// Dosimetria por fases (art. 68 do CP) no detalhe do tipo penal.
//
// Os modificadores são apresentados em BLOCOS SEPARADOS POR FASE — a separação
// não é estética: cada fase incide sobre uma base diferente e tem limites
// próprios (a 2ª fase é presa à moldura pela Súmula 231; a 3ª pode rompê-la).
// A pena definitiva apurada alimenta a pena concreta dos benefícios.

import React, {useEffect, useMemo, useState} from 'react';

import type {Crime} from '@site/src/lib/types';
import {MODIFICADORES, calcularDosimetria} from '@site/src/lib/dosimetria';
import {modificadoresAplicaveis, porFase} from '@site/src/lib/dosimetria/aplicaveis';
import type {Modificador, SelecaoModificador} from '@site/src/lib/dosimetria/types';

import styles from './styles.module.css';

const TITULO_FASE: Record<1 | 2 | 3, string> = {
  1: '1ª fase — pena-base (art. 59)',
  2: '2ª fase — agravantes e atenuantes (arts. 61-66)',
  3: '3ª fase — causas de aumento e diminuição',
};

const DICA_FASE: Record<1 | 2 | 3, string> = {
  1: 'Cada circunstância judicial desfavorável desloca 1/8 do intervalo da moldura. O resultado não ultrapassa o mínimo nem o máximo legal.',
  2: 'Cada agravante ou atenuante move 1/6 da pena-base. Súmula 231 do STJ: a atenuante não reduz a pena abaixo do mínimo legal.',
  3: 'A fração incide sobre a pena intermediária. Esta é a única fase que pode romper a moldura — para baixo (tentativa) ou para cima.',
};

function fmtFracao(f: number): string {
  const conhecidas: [number, string][] = [
    [1 / 8, '1/8'], [1 / 6, '1/6'], [1 / 4, '1/4'], [1 / 3, '1/3'],
    [1 / 2, '1/2'], [2 / 3, '2/3'],
  ];
  const achou = conhecidas.find(([v]) => Math.abs(v - f) < 0.005);
  return achou ? achou[1] : `${Math.round(f * 100)}%`;
}

function meses(v: number): string {
  const anos = Math.floor(v / 12);
  const m = Math.round((v - anos * 12) * 10) / 10;
  if (anos && m) return `${anos}a ${m}m`;
  if (anos) return `${anos} ano${anos > 1 ? 's' : ''}`;
  return `${m} m${m === 1 ? 'ês' : 'eses'}`;
}

export default function Dosimetria({
  crime,
  penaMin,
  penaMax,
  onPenaDefinitiva,
}: {
  crime: Crime;
  /** Moldura corrente (respeita a simulação legislativa das barras). */
  penaMin: number;
  penaMax: number;
  onPenaDefinitiva: (v: number | null) => void;
}) {
  const [sel, setSel] = useState<SelecaoModificador[]>([]);

  // Troca de tipo penal zera as escolhas — são do caso, não do catálogo.
  useEffect(() => {
    setSel([]);
  }, [crime.id]);

  const aplicaveis = useMemo(
    () => modificadoresAplicaveis(MODIFICADORES, crime),
    [crime.id],
  );

  // A dosimetria usa a moldura CORRENTE, para que a simulação legislativa
  // (barras de pena mínima/máxima) se propague às três fases.
  const molduraCorrente = useMemo(
    () => ({...crime, pena_min_meses: penaMin, pena_max_meses: penaMax}),
    [crime, penaMin, penaMax],
  );

  const resultado = useMemo(
    () => calcularDosimetria(molduraCorrente, sel),
    [molduraCorrente, sel],
  );

  // Só assume a pena concreta quando há algo marcado; sem seleção, a barra
  // manual do usuário continua no comando.
  useEffect(() => {
    onPenaDefinitiva(sel.length ? resultado.penaDefinitiva : null);
  }, [sel.length, resultado.penaDefinitiva]);

  const marcado = (id: string) => sel.some((s) => s.id === id);
  const alternar = (m: Modificador) =>
    setSel((p) =>
      p.some((s) => s.id === m.id)
        ? p.filter((s) => s.id !== m.id)
        : [...p, {id: m.id, fracao: m.fracao_min ?? undefined}],
    );
  const mudarFracao = (id: string, fracao: number) =>
    setSel((p) => p.map((s) => (s.id === id ? {...s, fracao} : s)));

  if (!crime.tem_pena_privativa) return null;

  const grupos = porFase(aplicaveis);

  return (
    <div className={styles.dosimetria}>
      <h4 className={styles.benefSecTitulo}>
        Dosimetria por fases — art. 68 do CP
      </h4>
      <p className={styles.simDica}>
        Marque as circunstâncias do caso. Cada fase é calculada sobre a base produzida
        pela anterior; a pena definitiva apurada passa a alimentar os benefícios abaixo.
      </p>

      <div className={styles.fasesGrid}>
        {grupos.map(({fase, itens}) => (
          <section key={fase} className={styles.faseBloco}>
            <h5 className={styles.faseTitulo}>{TITULO_FASE[fase]}</h5>
            <p className={styles.faseDica}>{DICA_FASE[fase]}</p>
            {itens.length === 0 ? (
              <p className={styles.faseVazia}>Nenhum modificador aplicável a este tipo.</p>
            ) : (
              <ul className={styles.faseLista}>
                {itens.map((m) => {
                  const escolhido = sel.find((s) => s.id === m.id);
                  const faixa = m.fracao_min !== null && m.fracao_max !== null &&
                    m.fracao_min !== m.fracao_max;
                  return (
                    <li key={m.id} className={styles.faseItem}>
                      <label className={styles.faseLabel} title={m.obs}>
                        <input
                          type="checkbox"
                          checked={marcado(m.id)}
                          onChange={() => alternar(m)}
                        />
                        <span className={styles.faseNome}>{m.nome}</span>
                        <span className={styles.faseDisp}>{m.dispositivo}</span>
                      </label>
                      {marcado(m.id) && faixa && (
                        <label className={styles.faseFracao}>
                          fração:
                          <input
                            type="range"
                            min={m.fracao_min!}
                            max={m.fracao_max!}
                            step={0.0167}
                            value={escolhido?.fracao ?? m.fracao_min!}
                            onChange={(e) => mudarFracao(m.id, +e.target.value)}
                          />
                          <strong>{fmtFracao(escolhido?.fracao ?? m.fracao_min!)}</strong>
                        </label>
                      )}
                    </li>
                  );
                })}
              </ul>
            )}
          </section>
        ))}
      </div>

      <div className={styles.dosiResultado}>
        <div className={styles.dosiEtapa}>
          <span className={styles.dosiRotulo}>Moldura</span>
          <strong>{meses(resultado.minimo)} – {meses(resultado.maximo)}</strong>
        </div>
        <span className={styles.dosiSeta}>→</span>
        <div className={styles.dosiEtapa}>
          <span className={styles.dosiRotulo}>Pena-base</span>
          <strong>{meses(resultado.penaBase)}</strong>
        </div>
        <span className={styles.dosiSeta}>→</span>
        <div className={styles.dosiEtapa}>
          <span className={styles.dosiRotulo}>Intermediária</span>
          <strong>{meses(resultado.penaIntermediaria)}</strong>
          {resultado.sumula231Aplicada && (
            <em className={styles.dosiNota}>limitada pela Súmula 231</em>
          )}
          {resultado.tetoAplicado && (
            <em className={styles.dosiNota}>limitada pelo máximo legal</em>
          )}
        </div>
        <span className={styles.dosiSeta}>→</span>
        <div className={`${styles.dosiEtapa} ${styles.dosiFinal}`}>
          <span className={styles.dosiRotulo}>Pena definitiva</span>
          <strong>{meses(resultado.penaDefinitiva)}</strong>
          {resultado.penaDefinitiva < resultado.minimo && (
            <em className={styles.dosiNota}>abaixo do mínimo (3ª fase)</em>
          )}
        </div>
      </div>

      {resultado.passos.length > 0 && (
        <details className={styles.dosiMemoria}>
          <summary>Memória de cálculo ({resultado.passos.length} passo(s))</summary>
          <ol>
            {resultado.passos.map((p, i) => (
              <li key={i}>
                <strong>{p.fase}ª fase</strong> · {p.modificador} ({p.dispositivo})
                {p.fracao !== null && <> · {fmtFracao(p.fracao)}</>} ·{' '}
                <span className={p.efeito >= 0 ? styles.efeitoMais : styles.efeitoMenos}>
                  {p.efeito >= 0 ? '+' : ''}{p.efeito} meses
                </span>
              </li>
            ))}
          </ol>
        </details>
      )}
    </div>
  );
}

// Concurso de pessoas (art. 29 do CP) — o papel do agente no fato.
//
// Fica em painel próprio, e não junto às causas de diminuição da 3ª fase, por
// uma razão de leitura: as outras causas são circunstâncias do FATO; esta é uma
// qualidade do AGENTE. É a lacuna que o sistema não sabia representar — o
// partícipe de participação reduzida condenado pelo mesmo tipo do autor.
//
// A escolha grava/remove o modificador `participacao-menor-importancia` na
// mesma seleção da dosimetria (estado erguido no Detalhe), de modo que a
// redução entre no encadeamento das três fases, e não por fora dele.

import React from 'react';

import type {SelecaoModificador} from '@site/src/lib/dosimetria/types';

import styles from './styles.module.css';

const ID_PARTICIPE = 'participacao-menor-importancia';

const PAPEIS = [
  {
    chave: 'autor',
    nome: 'Autor, coautor ou partícipe comum',
    dispositivo: 'CP, art. 29, caput',
    nota: 'Quem concorre para o crime incide nas penas a ele cominadas, na medida da sua culpabilidade. Sem redução própria.',
  },
  {
    chave: 'menor',
    nome: 'Partícipe de menor importância',
    dispositivo: 'CP, art. 29, §1º',
    nota: 'A pena é diminuída de um sexto a um terço. A redução entra na 3ª fase e pode levar a pena abaixo do mínimo.',
  },
] as const;

function fmtFracao(f: number): string {
  const conhecidas: [number, string][] = [
    [1 / 6, '1/6'], [1 / 5, '1/5'], [1 / 4, '1/4'], [1 / 3, '1/3'],
  ];
  const achou = conhecidas.find(([v]) => Math.abs(v - f) < 0.012);
  return achou ? achou[1] : `${Math.round(f * 100)}%`;
}

export default function ConcursoPessoas({
  sel,
  setSel,
}: {
  sel: SelecaoModificador[];
  setSel: React.Dispatch<React.SetStateAction<SelecaoModificador[]>>;
}) {
  const escolhido = sel.find((s) => s.id === ID_PARTICIPE);
  const papel = escolhido ? 'menor' : 'autor';

  const escolher = (chave: string) =>
    setSel((p) =>
      chave === 'menor'
        ? p.some((s) => s.id === ID_PARTICIPE)
          ? p
          : [...p, {id: ID_PARTICIPE, fracao: 1 / 6}]
        : p.filter((s) => s.id !== ID_PARTICIPE),
    );

  const mudarFracao = (fracao: number) =>
    setSel((p) => p.map((s) => (s.id === ID_PARTICIPE ? {...s, fracao} : s)));

  return (
    <div className={styles.concurso}>
      <h4 className={styles.benefSecTitulo}>Concurso de pessoas — art. 29</h4>
      <p className={styles.simDica}>
        Quando mais de um agente concorre para o mesmo fato, todos respondem pelo mesmo
        tipo — mas não pela mesma pena. Escolha o papel deste agente.
      </p>

      <ul className={styles.papelLista}>
        {PAPEIS.map((p) => (
          <li key={p.chave}>
            <label
              className={`${styles.papelOpcao} ${
                papel === p.chave ? styles.concursoAtiva : ''
              }`}>
              <input
                type="radio"
                name="papel-agente"
                checked={papel === p.chave}
                onChange={() => escolher(p.chave)}
              />
              <span className={styles.papelNome}>
                {p.nome}
                <em>{p.dispositivo}</em>
              </span>
            </label>
            {papel === p.chave && <p className={styles.papelNota}>{p.nota}</p>}
            {p.chave === 'menor' && papel === 'menor' && (
              <label className={styles.faseFracao}>
                redução:
                <input
                  type="range"
                  min={1 / 6}
                  max={1 / 3}
                  step={0.0167}
                  value={escolhido?.fracao ?? 1 / 6}
                  onChange={(e) => mudarFracao(+e.target.value)}
                />
                <strong>{fmtFracao(escolhido?.fracao ?? 1 / 6)}</strong>
              </label>
            )}
          </li>
        ))}
      </ul>

      <p className={styles.concursoNota}>
        A <strong>cooperação dolosamente distinta</strong> (art. 29, §2º) não se resolve
        aqui: quem quis participar de crime menos grave responde pela pena{' '}
        <em>daquele</em> crime, que tem linha própria no catálogo — consulte-a
        diretamente. As agravantes de quem <strong>dirige, coage ou paga</strong> pela
        execução (art. 62) estão na 2ª fase, acima.
      </p>
    </div>
  );
}

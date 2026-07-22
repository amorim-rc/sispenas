// Motor da dosimetria por fases (art. 68 do CP).
//
// A ordem das fases é normativa, não cosmética — cada uma incide sobre a base
// produzida pela anterior, e os limites são diferentes:
//
//   1ª  pena-base .......... mínimo + Σ(1/8 do intervalo por circunstância
//                            judicial desfavorável), PRESA à moldura
//   2ª  pena intermediária . pena-base ± Σ(fração da pena-base), PRESA à
//                            moldura — piso é a Súmula 231 do STJ
//   3ª  pena definitiva .... intermediária ± Σ(fração da intermediária),
//                            LIVRE: pode ficar abaixo do mínimo ou acima do
//                            máximo legal
//
// É essa assimetria da 3ª fase que permite, por exemplo, a tentativa levar a
// pena abaixo do mínimo cominado.

// Caminho relativo (e não o alias @site) para que o módulo resolva tanto no
// bundler do Docusaurus quanto no tsc/node do `npm run verificar`.
import brutos from '../../../data/modificadores.json';
import type {Crime} from '../types';
import type {
  Modificador,
  PassoCalculo,
  ResultadoConcurso,
  ResultadoDosimetria,
  SelecaoModificador,
} from './types';

export const MODIFICADORES = (brutos as {modificadores: Modificador[]}).modificadores;

export const POR_ID: Record<string, Modificador> = Object.fromEntries(
  MODIFICADORES.map((m) => [m.id, m]),
);

const limitar = (v: number, min: number, max: number) => Math.min(Math.max(v, min), max);
/** Arredonda a 1 casa, como a praxe forense (meses com décimo). */
const arred = (v: number) => Math.round(v * 10) / 10;

/** Fração efetiva de uma seleção: a escolhida, ou a mínima do modificador. */
function fracaoDe(sel: SelecaoModificador, m: Modificador): number {
  if (sel.fracao !== undefined) return sel.fracao;
  return m.fracao_min ?? 0;
}

/**
 * Percorre as três fases sobre a moldura do tipo penal.
 *
 * `selecoes` são os modificadores marcados pelo usuário; os de natureza
 * `concurso` são ignorados aqui (têm cálculo próprio em `calcularConcurso`).
 */
export function calcularDosimetria(
  crime: Crime,
  selecoes: SelecaoModificador[],
): ResultadoDosimetria {
  const minimo = crime.pena_min_meses;
  const maximo = crime.pena_max_meses;
  const intervalo = Math.max(maximo - minimo, 0);
  const passos: PassoCalculo[] = [];

  const ativos = selecoes
    .map((s) => ({sel: s, mod: POR_ID[s.id]}))
    .filter((x): x is {sel: SelecaoModificador; mod: Modificador} => Boolean(x.mod))
    .filter((x) => x.mod.natureza !== 'concurso');

  // ── 1ª fase — pena-base (art. 59) ─────────────────────────────────────────
  let penaBase = minimo;
  for (const {sel, mod} of ativos.filter((x) => x.mod.fase === 1)) {
    const fracao = fracaoDe(sel, mod);
    const efeito = intervalo * fracao;
    penaBase += efeito;
    passos.push({fase: 1, modificador: mod.nome, dispositivo: mod.dispositivo, fracao, efeito: arred(efeito)});
  }
  penaBase = arred(limitar(penaBase, minimo, maximo));

  // ── 2ª fase — agravantes e atenuantes (arts. 61-66) ───────────────────────
  let intermediaria = penaBase;
  for (const {sel, mod} of ativos.filter((x) => x.mod.fase === 2)) {
    const fracao = fracaoDe(sel, mod);
    const bruto = penaBase * fracao; // incide sempre sobre a PENA-BASE
    const efeito = mod.natureza === 'atenuante' ? -bruto : bruto;
    intermediaria += efeito;
    passos.push({fase: 2, modificador: mod.nome, dispositivo: mod.dispositivo, fracao, efeito: arred(efeito)});
  }
  const semLimite2 = intermediaria;
  intermediaria = arred(limitar(intermediaria, minimo, maximo));
  const sumula231Aplicada = semLimite2 < minimo;
  const tetoAplicado = semLimite2 > maximo;

  // ── 3ª fase — causas de aumento e diminuição ──────────────────────────────
  let definitiva = intermediaria;
  for (const {sel, mod} of ativos.filter((x) => x.mod.fase === 3)) {
    const fracao = fracaoDe(sel, mod);
    const bruto = intermediaria * fracao; // incide sobre a INTERMEDIÁRIA
    const efeito = mod.natureza === 'diminuicao' ? -bruto : bruto;
    definitiva += efeito;
    passos.push({fase: 3, modificador: mod.nome, dispositivo: mod.dispositivo, fracao, efeito: arred(efeito)});
  }
  // A 3ª fase não se prende à moldura; só não pode ser negativa.
  definitiva = arred(Math.max(definitiva, 0));

  return {
    minimo,
    maximo,
    penaBase,
    penaIntermediaria: intermediaria,
    penaDefinitiva: definitiva,
    sumula231Aplicada,
    tetoAplicado,
    passos,
  };
}

/**
 * Concurso de crimes (arts. 69-71) sobre penas JÁ definitivas.
 *
 * Regra do art. 70, par. único (concurso material benéfico): se a exasperação
 * resultar em pena maior que a soma do cúmulo material, aplica-se a soma.
 */
export function calcularConcurso(
  penas: number[],
  modalidade: 'material' | 'formal' | 'continuado',
  fracao = 1 / 6,
): ResultadoConcurso {
  const validas = penas.filter((p) => p > 0);
  const soma = arred(validas.reduce((a, b) => a + b, 0));
  const maior = validas.length ? Math.max(...validas) : 0;

  if (modalidade === 'material') {
    return {
      modalidade: 'Concurso material',
      dispositivo: 'CP, art. 69',
      total: soma,
      memoria: `Soma das ${validas.length} penas (cúmulo material).`,
    };
  }

  const exasperada = arred(maior * (1 + fracao));
  const rotulo = modalidade === 'formal' ? 'Concurso formal próprio' : 'Crime continuado';
  const disp = modalidade === 'formal' ? 'CP, art. 70' : 'CP, art. 71';
  const fracaoTxt = `${Math.round(fracao * 100)}%`;

  if (exasperada > soma) {
    return {
      modalidade: `${rotulo} (limitado pelo cúmulo material)`,
      dispositivo: `${disp}, c/c art. 70, par. único`,
      total: soma,
      memoria: `Maior pena (${maior}) + ${fracaoTxt} = ${exasperada}, que excede a soma ` +
        `(${soma}); pelo art. 70, par. único, aplica-se a soma.`,
    };
  }
  return {
    modalidade: rotulo,
    dispositivo: disp,
    total: exasperada,
    memoria: `Maior pena (${maior}) aumentada de ${fracaoTxt}.`,
  };
}

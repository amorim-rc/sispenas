// Construção do cenário de cálculo a partir de um tipo penal do catálogo.

import type {Cenario, Crime} from './types';

/**
 * Cenário inicial de um tipo penal: penas cominadas + características objetivas
 * lidas do catálogo, com o réu presumido primário e de bons antecedentes.
 *
 * Tudo o que é atributo do TIPO (hediondez, violência, culpa, resultado morte,
 * previsão de perdão judicial) vem do catálogo; o que é atributo do RÉU ou do
 * caso concreto (primariedade, confissão, reparação) recebe um padrão neutro e
 * é ajustável na simulação.
 */
export function cenarioFromCrime(c: Crime): Cenario {
  return {
    penaMin: c.pena_min_meses,
    penaMax: c.pena_max_meses,
    penaConcreta: c.pena_min_meses || c.pena_max_meses || 12,
    primario: true,
    reincidenteEspecifico: false,
    hediondo: c.hediondo === 'Sim',
    resultadoMorte: c.resultado_morte === true,
    violencia: c.violencia === 'Sim',
    graveAmeaca: c.grave_ameaca === 'Sim',
    confessou: false,
    reparouDano: false,
    bonsAntecedentes: true,
    culposo: c.elemento === 'Culposo',
    admiteTentativa: c.tentativa === 'Sim',
    perdaoJudicialPrevisto: c.perdao_judicial_previsto === true,
  };
}

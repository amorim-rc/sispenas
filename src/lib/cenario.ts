// Construção do cenário de cálculo a partir de um tipo penal do catálogo.

import type {Cenario, Crime} from './types';

/**
 * Cenário inicial de um tipo penal: penas cominadas + características objetivas
 * lidas do catálogo, com o réu presumido primário e de bons antecedentes.
 *
 * `resultadoMorte` inicia em `false` porque o catálogo ainda não registra, tipo a
 * tipo, a presença do resultado morte — é uma escolha do usuário na simulação
 * (ver docs/roadmap.md, v1.1.0).
 */
export function cenarioFromCrime(c: Crime): Cenario {
  return {
    penaMin: c.pena_min_meses,
    penaMax: c.pena_max_meses,
    penaConcreta: c.pena_min_meses || c.pena_max_meses || 12,
    primario: true,
    reincidenteEspecifico: false,
    hediondo: c.hediondo === 'Sim',
    resultadoMorte: false,
    violencia: c.violencia === 'Sim',
    graveAmeaca: c.grave_ameaca === 'Sim',
    confessou: false,
    reparouDano: false,
    bonsAntecedentes: true,
    culposo: c.elemento === 'Culposo',
    admiteTentativa: c.tentativa === 'Sim',
  };
}

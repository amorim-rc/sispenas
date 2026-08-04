// Construção do cenário de cálculo a partir de um tipo penal do catálogo.

import type {Cenario, Crime} from './types';
import {ehTituloXII} from './dosimetria/aplicaveis';

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
    // Feminicídio deriva do NOME do tipo, pela mesma razão que `resultado_morte`
    // (convenção C5): o `obs` descreve os demais parágrafos do artigo e produziria
    // falso positivo. É o que aciona a alínea "d" do art. 112, VI da LEP.
    feminicidio: /feminic[íi]dio/i.test(c.crime ?? ''),
    // Circunstância do caso concreto: parte-se de "não", e quem conhece os autos
    // marca na simulação.
    comandoOrgcrimUltraviolenta: false,
    // Topográfico, e por isso lido do próprio registro: basta o tipo estar nos
    // arts. 359-A a 359-T do CP. O art. 112 da LEP os ressalva sem perguntar se
    // a conduta foi violenta — o art. 359-L (abolição violenta) e o art. 359-M
    // (golpe de Estado) são violentos por definição típica e ainda assim entram.
    tituloXII: ehTituloXII(c.lei ?? '', c.artigo ?? ''),
    // Parte-se da lei vigente. Quem simula fato anterior marca na simulação.
    fatoAnteriorA15402: false,
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

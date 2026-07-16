// Busca reversa: dado UM benefício, quais tipos penais ele alcança?
//
// O fluxo direto ("Busca por tipo penal") fixa o tipo e varia os benefícios.
// Aqui o benefício é fixo — inclusive com seus parâmetros editados — e varremos
// o catálogo de tipos penais.
//
// PRESSUPOSTO METODOLÓGICO (importante)
// ─────────────────────────────────────
// Benefícios de natureza `concreto` dependem da pena fixada na SENTENÇA, que não
// é atributo do tipo penal. Para varrer o catálogo é preciso presumir uma pena
// concreta. O padrão é a PENA MÍNIMA COMINADA — hipótese do réu condenado no
// mínimo legal, a mais favorável e a de uso corrente na pesquisa empírica. O
// usuário pode trocá-la por pena máxima ou por um valor fixo.
//
// Benefícios de natureza `abstrato` não dependem dessa presunção: sua avaliação
// é exata a partir das penas cominadas.

import type {Cenario, Crime} from '../types';
import {cenarioFromCrime} from '../cenario';
import type {BeneficioDef, BeneficioResultado, Parametros, Status} from './types';
import {avaliarBeneficio} from './index';

/** De onde sai a pena concreta presumida na varredura do catálogo. */
export type BasePenaConcreta = 'minima' | 'maxima' | 'fixa';

export const BASE_LABEL: Record<BasePenaConcreta, string> = {
  minima: 'Pena mínima cominada',
  maxima: 'Pena máxima cominada',
  fixa: 'Valor fixo',
};

export const BASE_AJUDA: Record<BasePenaConcreta, string> = {
  minima:
    'Presume o réu condenado no mínimo legal — hipótese mais favorável e a de uso ' +
    'corrente na pesquisa empírica sobre acesso a benefícios.',
  maxima:
    'Presume o réu condenado no máximo legal — cenário de reprovação mais severa; ' +
    'mede o alcance mínimo do benefício.',
  fixa:
    'Aplica a mesma pena concreta a todos os tipos penais. Útil para isolar o efeito ' +
    'de um patamar de pena específico sobre o catálogo inteiro.',
};

/**
 * Circunstâncias do RÉU aplicadas a todo o catálogo durante a varredura.
 *
 * Só entram aqui atributos que não pertencem ao tipo penal. Hediondez,
 * violência, culpa, resultado morte e previsão de perdão judicial são lidos do
 * catálogo, tipo a tipo — não são alavancas globais.
 */
export interface CenarioReverso {
  base: BasePenaConcreta;
  /** Pena concreta em meses, usada quando `base === 'fixa'`. */
  penaFixaMeses: number;
  reincidenteEspecifico: boolean;
  confessou: boolean;
  reparouDano: boolean;
  bonsAntecedentes: boolean;
}

export function cenarioReversoPadrao(): CenarioReverso {
  return {
    base: 'minima',
    penaFixaMeses: 24,
    reincidenteEspecifico: false,
    confessou: false,
    reparouDano: false,
    bonsAntecedentes: true,
  };
}

/**
 * Tipos penais que entram nas estatísticas de alcance dos benefícios.
 *
 * Benefícios se medem por patamar de pena, então um tipo sem pena privativa
 * cominada satisfaria qualquer teto e seria contado como "cabível". Hoje a
 * única exceção é o art. 28 da Lei 11.343/06, cujas sanções (advertência,
 * prestação de serviços, medida educativa) não são privativas de liberdade.
 */
export function crimesComPenaPrivativa(crimes: Crime[]): Crime[] {
  return crimes.filter((c) => c.tem_pena_privativa !== false);
}

function penaConcretaPresumida(c: Crime, rev: CenarioReverso): number {
  switch (rev.base) {
    case 'minima':
      return c.pena_min_meses || c.pena_max_meses;
    case 'maxima':
      return c.pena_max_meses || c.pena_min_meses;
    case 'fixa':
      return rev.penaFixaMeses;
  }
}

/**
 * Cenário de um tipo penal sob as circunstâncias globais da busca reversa.
 *
 * `cenarioFromCrime` já traz os atributos do tipo (inclusive `resultadoMorte` e
 * `perdaoJudicialPrevisto`, lidos do catálogo); aqui só se sobrepõem a pena
 * concreta presumida e as circunstâncias do réu.
 */
export function cenarioParaCrime(c: Crime, rev: CenarioReverso): Cenario {
  return {
    ...cenarioFromCrime(c),
    penaConcreta: penaConcretaPresumida(c, rev),
    primario: !rev.reincidenteEspecifico,
    reincidenteEspecifico: rev.reincidenteEspecifico,
    confessou: rev.confessou,
    reparouDano: rev.reparouDano,
    bonsAntecedentes: rev.bonsAntecedentes,
  };
}

export interface LinhaReversa {
  crime: Crime;
  resultado: BeneficioResultado;
}

/** Avalia um benefício (com seus parâmetros correntes) contra todo o catálogo. */
export function avaliarCatalogo(
  def: BeneficioDef,
  params: Parametros,
  crimes: Crime[],
  rev: CenarioReverso,
): LinhaReversa[] {
  return crimes.map((crime) => ({
    crime,
    resultado: avaliarBeneficio(def, cenarioParaCrime(crime, rev), params),
  }));
}

export type Contagem = Record<Status, number>;

export function contar(linhas: LinhaReversa[]): Contagem {
  const out: Contagem = {cabivel: 0, condicional: 0, incabivel: 0};
  for (const l of linhas) out[l.resultado.status] += 1;
  return out;
}

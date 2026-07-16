// Motor de cálculo de benefícios penais — SISPENAS.
//
// API pública do módulo. `calcularBeneficios(cenario)` mantém a assinatura usada
// pela "Busca por tipo penal"; o segundo argumento (opcional) permite avaliar o
// catálogo com parâmetros editados, base da "Busca por benefício".
//
// AVISO: implementação para fins de PESQUISA. Simplifica controvérsias
// doutrinárias e jurisprudenciais. Não substitui análise jurídica.

import type {Cenario} from '../types';
import type {BeneficioDef, BeneficioResultado, Categoria, Parametros} from './types';
import {valoresPadrao} from './types';
import {CATALOGO, POR_ID} from './catalogo';

export type {
  Avaliacao,
  BeneficioDef,
  BeneficioResultado,
  Categoria,
  Limiar,
  Natureza,
  ParametroDef,
  ParamTipo,
  Parametros,
  Status,
} from './types';
export {foiEditado, valoresPadrao} from './types';
export {CATALOGO, POR_ID} from './catalogo';

/** Avalia um único benefício, com parâmetros próprios ou padrão. */
export function avaliarBeneficio(
  def: BeneficioDef,
  c: Cenario,
  params?: Parametros,
): BeneficioResultado {
  const p = params ?? valoresPadrao(def);
  return {
    id: def.id,
    nome: def.nome,
    fundamento: def.fundamento,
    categoria: def.categoria,
    natureza: def.natureza,
    ...def.avaliar(c, p),
  };
}

/**
 * Avalia o catálogo inteiro para um cenário.
 *
 * @param overrides parâmetros editados, por id de benefício. Benefícios ausentes
 *   do mapa são avaliados com os valores legais padrão.
 */
export function calcularBeneficios(
  c: Cenario,
  overrides?: Record<string, Parametros>,
): BeneficioResultado[] {
  return CATALOGO.map((def) => avaliarBeneficio(def, c, overrides?.[def.id]));
}

export function getBeneficio(id: string): BeneficioDef | undefined {
  return POR_ID[id];
}

export const CATEGORIA_LABEL: Record<Categoria, string> = {
  processual: 'Benefícios processuais (pena em abstrato)',
  aplicacao: 'Aplicação da pena (pena concreta)',
  execucao: 'Execução penal',
};

/** Rótulo curto, para chips e listagens. */
export const CATEGORIA_CURTA: Record<Categoria, string> = {
  processual: 'Processual',
  aplicacao: 'Aplicação',
  execucao: 'Execução',
};

export const NATUREZA_LABEL: Record<string, string> = {
  abstrato: 'Pena em abstrato',
  concreto: 'Pena concreta',
  incondicionado: 'Independe da pena',
};

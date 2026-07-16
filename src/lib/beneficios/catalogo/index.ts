// Catálogo de benefícios penais — registro único.
//
// A ORDEM deste array define a ordem de exibição dentro de cada categoria.
// Para acrescentar um benefício, crie o `BeneficioDef` no arquivo da categoria
// correspondente e inclua-o no array exportado por aquele arquivo.

import type {BeneficioDef} from '../types';
import {PROCESSUAIS} from './processuais';
import {APLICACAO} from './aplicacao';
import {EXECUCAO} from './execucao';

export const CATALOGO: BeneficioDef[] = [...PROCESSUAIS, ...APLICACAO, ...EXECUCAO];

export const POR_ID: Record<string, BeneficioDef> = Object.fromEntries(
  CATALOGO.map((b) => [b.id, b]),
);

export * from './processuais';
export * from './aplicacao';
export * from './execucao';

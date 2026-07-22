// Modelo da dosimetria por fases (art. 68 do CP) — v1.2.0.
//
// Um MODIFICADOR não é tipo penal: é um componente que desloca a moldura de
// pena. Vive em data/modificadores.json e é aplicado sobre a linha do catálogo
// no momento da consulta — por isso a dosimetria é MENOR, não MAIOR: nenhum
// campo de crimes.json muda.

export type Fase = 1 | 2 | 3 | 'concurso';

export type NaturezaModificador =
  | 'judicial'    // 1ª fase — circunstâncias do art. 59
  | 'agravante'   // 2ª fase
  | 'atenuante'   // 2ª fase
  | 'aumento'     // 3ª fase
  | 'diminuicao'  // 3ª fase
  | 'concurso';   // combinador (arts. 69-71)

/** Base sobre a qual a fração incide — determinada pela fase. */
export type BaseIncidencia = 'intervalo' | 'pena_base' | 'pena_provisoria' | 'especial';

export type Escopo =
  | {tipo: 'geral'}
  | {tipo: 'lei'; valor: string}
  | {tipo: 'titulo'; lei: string; valor: string}
  | {tipo: 'tipos_por_artigo'; lei: string; artigos: string[]}
  | {tipo: 'tipos'; ids: number[]}
  | {tipo: 'combinador'};

export interface Modificador {
  id: string;
  nome: string;
  dispositivo: string;
  natureza: NaturezaModificador;
  fase: Fase;
  sobre: BaseIncidencia;
  /** Fração mínima (0.125 = 1/8); null quando o quantum não é tabelado. */
  fracao_min: number | null;
  fracao_max: number | null;
  /** Súmula 231 do STJ — só na 2ª fase. */
  piso_minimo: boolean;
  escopo: Escopo;
  /** Pré-requisito do tipo penal para o modificador ser oferecido. */
  condicao?: string;
  obs?: string;
}

/** Um modificador escolhido pelo usuário, com a fração aplicada. */
export interface SelecaoModificador {
  id: string;
  /** Fração dentro de [fracao_min, fracao_max]; ausente = usa a mínima. */
  fracao?: number;
}

/** Uma linha da memória de cálculo — o "porquê" de cada deslocamento. */
export interface PassoCalculo {
  fase: Fase;
  modificador: string;
  dispositivo: string;
  fracao: number | null;
  /** Efeito em meses (positivo aumenta, negativo reduz). */
  efeito: number;
}

export interface ResultadoDosimetria {
  /** Moldura original do tipo. */
  minimo: number;
  maximo: number;
  /** 1ª fase — limitada à moldura. */
  penaBase: number;
  /** 2ª fase — limitada à moldura (Súmula 231 no piso). */
  penaIntermediaria: number;
  /** 3ª fase — pode ultrapassar a moldura em ambos os sentidos. */
  penaDefinitiva: number;
  /** Verdadeiro se a Súmula 231 impediu a redução abaixo do mínimo. */
  sumula231Aplicada: boolean;
  /** Verdadeiro se a 2ª fase foi limitada pelo máximo da moldura. */
  tetoAplicado: boolean;
  passos: PassoCalculo[];
}

/** Resultado do concurso (arts. 69-71) sobre penas já definitivas. */
export interface ResultadoConcurso {
  modalidade: string;
  dispositivo: string;
  total: number;
  /** Explicação do cálculo (soma, maior + fração, teto do art. 70 par. único). */
  memoria: string;
}

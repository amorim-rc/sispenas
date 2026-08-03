// Modelo de dados do catálogo de tipos penais SISPENAS.

export type PenaPrivativa = 'Reclusão' | 'Detenção' | 'Prisão simples' | 'Nenhuma';
export type MultaRegime = 'cumulativa' | 'alternativa' | 'isolada' | 'nenhuma';
export type SimNao = 'Sim' | 'Não' | '—';

/**
 * Sanção de tipo penal que não comina pena privativa de liberdade.
 * Hoje só o art. 28 da Lei 11.343/06 (porte para consumo pessoal).
 */
export interface SancaoNaoPrivativa {
  /** Inciso do dispositivo que a comina (ex.: "II"). */
  inciso: string;
  sancao: string;
}

export interface Crime {
  id: number;
  lei: string;
  artigo: string;
  crime: string;
  /** Pena mínima em MESES. */
  pena_min: number;
  /** Pena máxima em MESES. */
  pena_max: number;
  tipo_pena: string;
  acao: string;
  hediondo: SimNao;
  /**
   * Quando a hediondez depende de circunstância do CASO, e não do tipo: o
   * homicídio do art. 121 só é hediondo se praticado em atividade típica de
   * grupo de extermínio. Aqui fica a condição, em texto; `hediondo` permanece
   * "Não", e quem marca é quem conhece o caso, na simulação.
   */
  hediondo_condicao?: string;
  /** Mesma ideia para a ação penal (art. 161, §3º: privada se a propriedade é particular). */
  acao_condicao?: string;
  elemento: string;
  tentativa: SimNao;
  violencia: SimNao;
  grave_ameaca: SimNao;
  obs: string;
  // ── Campos derivados de tipo_pena/obs por scripts/transform_data.py ──
  pena_privativa: PenaPrivativa;
  tem_multa: boolean;
  multa_regime: MultaRegime;
  infracao_menor_potencial: boolean;
  derivado_auto: boolean;
  /** Derivados de `hediondo_condicao`/`acao_condicao`: a classificação depende do caso. */
  hediondo_condicional: boolean;
  acao_condicional: boolean;
  /** Pena mínima canônica em meses (dias/anos já convertidos). */
  pena_min_meses: number;
  /** Pena máxima canônica em meses (dias/anos já convertidos). */
  pena_max_meses: number;
  /** Rótulo de exibição na unidade natural (ex.: "15 dias"). */
  pena_min_rotulo: string;
  /** Rótulo de exibição na unidade natural (ex.: "6 meses"). */
  pena_max_rotulo: string;
  /** Faixa completa para exibição (ex.: "15 dias a 6 meses", "1 a 5 anos"). */
  pena_faixa_rotulo: string;
  /** True se a unidade veio do parser do texto (senão, fallback em meses). */

  // ── Qualidade e integração com o motor de benefícios ──
  /**
   * O tipo comina pena privativa de liberdade? Só quem tem entra nas
   * estatísticas de alcance dos benefícios, que se medem por patamar de pena.
   * A exceção é o art. 28 da Lei 11.343/06, cujas sanções são não privativas.
   */
  tem_pena_privativa: boolean;
  /** Sanções próprias dos tipos sem pena privativa (art. 28, I a III, Lei 11.343/06). */
  sancoes_nao_privativas: SancaoNaoPrivativa[];
  /** Qualificado pelo resultado morte (art. 112, VI e VIII, LEP). */
  resultado_morte: boolean;
  /** True se `resultado_morte` veio da heurística, não de revisão manual. */
  resultado_morte_derivado: boolean;
  /** Há previsão legal expressa de perdão judicial para o tipo (art. 107, IX, CP). */
  perdao_judicial_previsto: boolean;
  /** Identidade do dispositivo (lei + artigo), para detectar repetições. */
  chave_dispositivo: string;
  /** O mesmo dispositivo aparece em mais de um registro. */
  duplicata: boolean;
  /** As cópias do dispositivo divergem em pena ou hediondez — contradição a revisar. */
  duplicata_divergente: boolean;
  duplicata_ids: number[];
}

/** Parâmetros do caso concreto usados no cálculo dinâmico de benefícios. */
export interface Cenario {
  /** Pena mínima em meses (permite simular alteração legislativa). */
  penaMin: number;
  /** Pena máxima em meses (permite simular alteração legislativa). */
  penaMax: number;
  /** Pena concreta aplicada em meses (para benefícios de execução). */
  penaConcreta: number;
  primario: boolean;
  reincidenteEspecifico: boolean;
  hediondo: boolean;
  resultadoMorte: boolean;
  /**
   * O tipo é feminicídio (art. 121-A do CP). Atributo do TIPO, lido do catálogo
   * como `resultadoMorte`: o art. 112, VI, "d" da LEP (alínea incluída pela Lei
   * 15.358/2026) exige 75% da pena e VEDA o livramento condicional ao primário
   * condenado por feminicídio.
   */
  feminicidio: boolean;
  /**
   * O condenado exercia comando, individual ou coletivo, de organização
   * criminosa ultraviolenta estruturada para a prática de crime hediondo ou
   * equiparado — art. 112, VI, "b" da LEP, na redação da Lei 15.358/2026.
   * Circunstância do CASO, não do tipo: só quem conhece os autos marca.
   */
  comandoOrgcrimUltraviolenta: boolean;
  violencia: boolean;
  graveAmeaca: boolean;
  confessou: boolean;
  reparouDano: boolean;
  bonsAntecedentes: boolean;
  /** Crime culposo: afasta o teto de pena da substituição (art. 44, I, parte final, CP). */
  culposo: boolean;
  /** Tipo admite tentativa: pressuposto da desistência voluntária/arrependimento eficaz. */
  admiteTentativa: boolean;
  /**
   * Há previsão legal expressa de perdão judicial para o tipo. Não se infere do
   * elemento culposo: o perdão só existe onde a lei o prevê e não se estende por
   * analogia (art. 107, IX, CP).
   */
  perdaoJudicialPrevisto: boolean;
}

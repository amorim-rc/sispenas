// Motor de cálculo de benefícios penais — SISPENAS.
//
// Funções puras: recebem o cenário (pena em abstrato/concreta + características)
// e devolvem, para cada benefício, se é cabível e o fundamento legal.
// Todas as penas estão em MESES.
//
// AVISO: implementação para fins de PESQUISA. Simplifica controvérsias
// doutrinárias e jurisprudenciais. Não substitui análise jurídica.

import type {Cenario} from './types';
import {formatPena, formatFracao} from './format';

export type Status = 'cabivel' | 'incabivel' | 'condicional';
export type Categoria = 'processual' | 'aplicacao' | 'execucao';

export interface Limiar {
  descricao: string;
  /** Valor de referência do cenário (meses). */
  referenciaMeses: number;
  /** Limiar legal (meses). */
  limiarMeses: number;
  /** Distância até perder/ganhar o benefício (meses); negativo = fora por X. */
  folgaMeses: number;
}

export interface BeneficioResultado {
  id: string;
  nome: string;
  fundamento: string;
  categoria: Categoria;
  status: Status;
  resumo: string;
  detalhes: string[];
  limiar?: Limiar;
}

const ANO = 12;

// ─────────────────────────────────────────────────────────────────────────
// Benefícios processuais (dependem da pena em ABSTRATO)
// ─────────────────────────────────────────────────────────────────────────

function transacaoPenal(c: Cenario): BeneficioResultado {
  const limite = 2 * ANO;
  const cabivel = c.penaMax <= limite;
  const detalhes = [
    'Infração de menor potencial ofensivo (IMPO): pena máxima não superior a 2 anos.',
    'Proposta pelo Ministério Público antes do oferecimento da denúncia.',
    'Vedado em casos de violência doméstica e familiar contra a mulher (Súmula 536 STJ).',
  ];
  return {
    id: 'transacao',
    nome: 'Transação penal',
    fundamento: 'Art. 76, Lei 9.099/95',
    categoria: 'processual',
    status: cabivel ? (c.violencia ? 'condicional' : 'cabivel') : 'incabivel',
    resumo: cabivel
      ? 'Pena máxima ≤ 2 anos → infração de menor potencial ofensivo.'
      : 'Pena máxima acima de 2 anos.',
    detalhes,
    limiar: {
      descricao: 'Pena máxima ≤ 2 anos',
      referenciaMeses: c.penaMax,
      limiarMeses: limite,
      folgaMeses: limite - c.penaMax,
    },
  };
}

function suspensaoProcesso(c: Cenario): BeneficioResultado {
  const limite = 1 * ANO;
  const cabivel = c.penaMin <= limite;
  return {
    id: 'sursis-processual',
    nome: 'Suspensão condicional do processo',
    fundamento: 'Art. 89, Lei 9.099/95',
    categoria: 'processual',
    status: cabivel ? (c.violencia ? 'condicional' : 'cabivel') : 'incabivel',
    resumo: cabivel
      ? 'Pena mínima ≤ 1 ano.'
      : 'Pena mínima acima de 1 ano.',
    detalhes: [
      'Cabível quando a pena mínima cominada for igual ou inferior a 1 ano.',
      'Período de prova de 2 a 4 anos, com condições (Art. 89, §1º).',
      'Vedado em violência doméstica e familiar contra a mulher (Súmula 536 STJ).',
    ],
    limiar: {
      descricao: 'Pena mínima ≤ 1 ano',
      referenciaMeses: c.penaMin,
      limiarMeses: limite,
      folgaMeses: limite - c.penaMin,
    },
  };
}

function anpp(c: Cenario): BeneficioResultado {
  const limite = 4 * ANO;
  const dentroPena = c.penaMin < limite;
  const semViolencia = !c.violencia && !c.graveAmeaca;
  let status: Status = 'incabivel';
  const detalhes = [
    'Pena mínima inferior a 4 anos.',
    'Infração cometida sem violência ou grave ameaça à pessoa.',
    'Confissão formal e circunstanciada do investigado.',
    'Vedado a reincidentes e quando cabível transação penal (Art. 28-A, §2º).',
  ];
  let resumo: string;
  if (dentroPena && semViolencia) {
    status = c.confessou ? 'cabivel' : 'condicional';
    resumo = c.confessou
      ? 'Requisitos objetivos preenchidos.'
      : 'Requisitos objetivos preenchidos; depende de confissão formal.';
  } else if (!dentroPena) {
    resumo = 'Pena mínima igual ou superior a 4 anos.';
  } else {
    resumo = 'Infração praticada com violência ou grave ameaça.';
  }
  return {
    id: 'anpp',
    nome: 'Acordo de não persecução penal (ANPP)',
    fundamento: 'Art. 28-A, CPP',
    categoria: 'processual',
    status,
    resumo,
    detalhes,
    limiar: {
      descricao: 'Pena mínima < 4 anos',
      referenciaMeses: c.penaMin,
      limiarMeses: limite,
      folgaMeses: limite - c.penaMin,
    },
  };
}

// ─────────────────────────────────────────────────────────────────────────
// Benefícios de APLICAÇÃO da pena (dependem da pena CONCRETA)
// ─────────────────────────────────────────────────────────────────────────

function substituicaoPRD(c: Cenario): BeneficioResultado {
  const limite = 4 * ANO;
  const dentroPena = c.penaConcreta <= limite;
  const semViolencia = !c.violencia && !c.graveAmeaca;
  const cabivel = dentroPena && semViolencia && !c.reincidenteEspecifico;
  return {
    id: 'substituicao',
    nome: 'Substituição por penas restritivas de direitos',
    fundamento: 'Art. 44, CP',
    categoria: 'aplicacao',
    status: cabivel ? 'cabivel' : 'incabivel',
    resumo: !dentroPena
      ? 'Pena concreta superior a 4 anos.'
      : !semViolencia
        ? 'Crime doloso com violência ou grave ameaça.'
        : c.reincidenteEspecifico
          ? 'Reincidência específica.'
          : 'Pena concreta ≤ 4 anos, crime sem violência/grave ameaça.',
    detalhes: [
      'Pena privativa não superior a 4 anos e crime cometido sem violência ou grave ameaça (crime doloso).',
      'Crimes culposos: cabível qualquer que seja a pena.',
      'Réu não reincidente em crime doloso (reincidente não específico: possível se socialmente recomendável, Art. 44, §3º).',
    ],
    limiar: {
      descricao: 'Pena concreta ≤ 4 anos',
      referenciaMeses: c.penaConcreta,
      limiarMeses: limite,
      folgaMeses: limite - c.penaConcreta,
    },
  };
}

function sursisPena(c: Cenario): BeneficioResultado {
  const limite = 2 * ANO;
  const limiteEtario = 4 * ANO;
  const cabivel = c.penaConcreta <= limite && !c.reincidenteEspecifico;
  const cabivelEtario = c.penaConcreta <= limiteEtario;
  return {
    id: 'sursis-pena',
    nome: 'Suspensão condicional da pena (sursis)',
    fundamento: 'Art. 77, CP',
    categoria: 'aplicacao',
    status: cabivel ? 'cabivel' : cabivelEtario ? 'condicional' : 'incabivel',
    resumo: cabivel
      ? 'Pena concreta ≤ 2 anos.'
      : cabivelEtario
        ? 'Sursis etário/humanitário: pena ≤ 4 anos (maior de 70 anos ou por saúde).'
        : 'Pena concreta acima do limite do sursis.',
    detalhes: [
      'Sursis comum: pena privativa não superior a 2 anos, réu não reincidente em crime doloso.',
      'Sursis etário: pena ≤ 4 anos para condenado maior de 70 anos.',
      'Sursis humanitário: pena ≤ 4 anos por razões de saúde.',
      'Subsidiário à substituição por PRD (Art. 77, III).',
    ],
    limiar: {
      descricao: 'Pena concreta ≤ 2 anos (comum)',
      referenciaMeses: c.penaConcreta,
      limiarMeses: limite,
      folgaMeses: limite - c.penaConcreta,
    },
  };
}

function regimeInicial(c: Cenario): BeneficioResultado {
  let regime: string;
  if (c.penaConcreta > 8 * ANO) regime = 'Fechado';
  else if (c.penaConcreta > 4 * ANO) regime = c.reincidenteEspecifico ? 'Fechado' : 'Semiaberto';
  else regime = c.reincidenteEspecifico ? 'Semiaberto' : 'Aberto';

  const detalhes = [
    'Pena superior a 8 anos: regime inicial fechado.',
    'Pena superior a 4 e até 8 anos: semiaberto (não reincidente).',
    'Pena até 4 anos: aberto (não reincidente).',
  ];
  if (c.hediondo) {
    detalhes.push(
      'Crimes hediondos/equiparados: na prática, regime inicial fechado; o STF (HC 111.840) afastou a obrigatoriedade automática — deve haver fundamentação.',
    );
    regime = c.penaConcreta > 4 * ANO ? 'Fechado' : regime;
  }
  return {
    id: 'regime',
    nome: 'Regime inicial de cumprimento',
    fundamento: 'Art. 33, §2º e §3º, CP',
    categoria: 'aplicacao',
    status: 'cabivel',
    resumo: `Regime inicial: ${regime}.`,
    detalhes,
  };
}

// ─────────────────────────────────────────────────────────────────────────
// Benefícios de EXECUÇÃO (dependem da pena concreta + tempo)
// ─────────────────────────────────────────────────────────────────────────

function progressao(c: Cenario): BeneficioResultado {
  const comViolencia = c.violencia || c.graveAmeaca;
  let fracao: number;
  let inciso: string;
  if (c.hediondo && c.resultadoMorte && c.reincidenteEspecifico) {
    fracao = 0.7; inciso = 'VIII — reincidente específico, hediondo com resultado morte (livramento vedado)';
  } else if (c.hediondo && c.resultadoMorte) {
    fracao = 0.5; inciso = 'VI — primário, hediondo com resultado morte (livramento vedado)';
  } else if (c.hediondo && c.reincidenteEspecifico) {
    fracao = 0.6; inciso = 'VII — reincidente, hediondo';
  } else if (c.hediondo) {
    fracao = 0.4; inciso = 'V — primário, hediondo/equiparado';
  } else if (comViolencia && c.reincidenteEspecifico) {
    fracao = 0.3; inciso = 'IV — reincidente, crime com violência/grave ameaça';
  } else if (comViolencia) {
    fracao = 0.25; inciso = 'III — primário, crime com violência/grave ameaça';
  } else if (c.reincidenteEspecifico) {
    fracao = 0.2; inciso = 'II — reincidente, sem violência/grave ameaça';
  } else {
    fracao = 0.16; inciso = 'I — primário, sem violência/grave ameaça';
  }
  const tempo = c.penaConcreta * fracao;
  return {
    id: 'progressao',
    nome: 'Progressão de regime',
    fundamento: 'Art. 112, LEP (Lei 13.964/2019)',
    categoria: 'execucao',
    status: 'cabivel',
    resumo: `Fração de ${(fracao * 100).toFixed(0)}% → ${formatPena(tempo)} de cumprimento.`,
    detalhes: [
      `Percentual aplicável: ${inciso}.`,
      `Tempo necessário sobre a pena de ${formatPena(c.penaConcreta)}: ${formatPena(tempo)}.`,
      'Requisito subjetivo: boa conduta carcerária (Art. 112, §1º).',
    ],
  };
}

function livramento(c: Cenario): BeneficioResultado {
  const minimo = 2 * ANO;
  if (c.penaConcreta < minimo) {
    return {
      id: 'livramento',
      nome: 'Livramento condicional',
      fundamento: 'Art. 83, CP',
      categoria: 'execucao',
      status: 'incabivel',
      resumo: 'Exige pena privativa igual ou superior a 2 anos.',
      detalhes: ['Pressuposto objetivo: pena privativa de liberdade igual ou superior a 2 anos.'],
    };
  }
  if (c.hediondo && c.reincidenteEspecifico) {
    return {
      id: 'livramento',
      nome: 'Livramento condicional',
      fundamento: 'Art. 83, V, CP',
      categoria: 'execucao',
      status: 'incabivel',
      resumo: 'Vedado ao reincidente específico em crime hediondo.',
      detalhes: ['Art. 83, V, CP: vedado para reincidente específico em crimes hediondos ou equiparados.'],
    };
  }
  let fracao: number;
  let base: string;
  if (c.hediondo) { fracao = 2 / 3; base = 'crime hediondo/equiparado (2/3)'; }
  else if (c.reincidenteEspecifico) { fracao = 1 / 2; base = 'reincidente em crime doloso (1/2)'; }
  else { fracao = 1 / 3; base = 'primário e bons antecedentes (1/3)'; }
  const tempo = c.penaConcreta * fracao;
  return {
    id: 'livramento',
    nome: 'Livramento condicional',
    fundamento: 'Art. 83, CP',
    categoria: 'execucao',
    status: 'cabivel',
    resumo: `Fração de ${formatFracao(fracao)} → ${formatPena(tempo)} cumpridos.`,
    detalhes: [
      `Fração aplicável: ${base}.`,
      `Tempo mínimo de cumprimento: ${formatPena(tempo)}.`,
      'Requisitos: bom comportamento, aptidão para o trabalho e reparação do dano (salvo impossibilidade).',
    ],
  };
}

function prescricao(c: Cenario): BeneficioResultado {
  function prazo(penaMeses: number): number {
    if (penaMeses > 12 * ANO) return 20 * ANO;
    if (penaMeses > 8 * ANO) return 16 * ANO;
    if (penaMeses > 4 * ANO) return 12 * ANO;
    if (penaMeses > 2 * ANO) return 8 * ANO;
    if (penaMeses >= 1 * ANO) return 4 * ANO;
    return 3 * ANO;
  }
  const abstrata = prazo(c.penaMax);
  const concreta = c.penaConcreta > 0 ? prazo(c.penaConcreta) : null;
  return {
    id: 'prescricao',
    nome: 'Prescrição da pretensão punitiva',
    fundamento: 'Art. 109, CP',
    categoria: 'execucao',
    status: 'cabivel',
    resumo: `Em abstrato (pena máx.): ${formatPena(abstrata)}.`,
    detalhes: [
      `Prescrição em abstrato, pela pena máxima de ${formatPena(c.penaMax)}: ${formatPena(abstrata)}.`,
      concreta
        ? `Prescrição pela pena concreta de ${formatPena(c.penaConcreta)}: ${formatPena(concreta)}.`
        : 'Informe uma pena concreta para calcular a prescrição retroativa/executória.',
      'Redução pela metade se o agente é menor de 21 na data do fato ou maior de 70 na sentença (Art. 115).',
    ],
  };
}

function detracao(): BeneficioResultado {
  return {
    id: 'detracao',
    nome: 'Detração penal',
    fundamento: 'Art. 42, CP',
    categoria: 'execucao',
    status: 'cabivel',
    resumo: 'Desconto do tempo de prisão provisória/internação.',
    detalhes: [
      'Computa-se na pena privativa e na medida de segurança o tempo de prisão provisória, administrativa ou internação.',
      'Aplicável a qualquer tipo penal; independe da quantidade de pena.',
    ],
  };
}

function remicao(): BeneficioResultado {
  return {
    id: 'remicao',
    nome: 'Remição de pena',
    fundamento: 'Art. 126, LEP',
    categoria: 'execucao',
    status: 'cabivel',
    resumo: 'Trabalho (1 dia/3) e estudo (1 dia/12h).',
    detalhes: [
      'Trabalho: 1 dia de pena remido a cada 3 dias trabalhados (regime fechado e semiaberto).',
      'Estudo: 1 dia de pena remido a cada 12 horas de frequência escolar (qualquer regime).',
      'Aplicável a qualquer tipo penal.',
    ],
  };
}

function saidaTemporaria(c: Cenario): BeneficioResultado {
  const fracao = c.reincidenteEspecifico ? 1 / 4 : 1 / 6;
  const tempo = c.penaConcreta * fracao;
  return {
    id: 'saida-temporaria',
    nome: 'Saída temporária',
    fundamento: 'Art. 122, LEP',
    categoria: 'execucao',
    status: 'condicional',
    resumo: `Regime semiaberto após ${formatFracao(fracao)} da pena (${formatPena(tempo)}).`,
    detalhes: [
      'Exclusiva do regime semiaberto.',
      `Cumprimento mínimo: ${formatFracao(fracao)} da pena (${c.reincidenteEspecifico ? 'reincidente' : 'primário'}).`,
      'Depende de comportamento adequado e compatibilidade com os objetivos da pena.',
    ],
  };
}

function indulto(c: Cenario): BeneficioResultado {
  return {
    id: 'indulto',
    nome: 'Indulto e comutação',
    fundamento: 'Art. 84, CP + decreto presidencial anual',
    categoria: 'execucao',
    status: c.hediondo ? 'incabivel' : 'condicional',
    resumo: c.hediondo
      ? 'Vedado a crimes hediondos e equiparados.'
      : 'Depende dos requisitos do decreto anual.',
    detalhes: [
      'Concedido por decreto presidencial, com requisitos variáveis a cada ano.',
      'Vedado a crimes hediondos, tortura, tráfico e terrorismo (Art. 5º, XLIII, CF).',
    ],
  };
}

// ─────────────────────────────────────────────────────────────────────────

export function calcularBeneficios(c: Cenario): BeneficioResultado[] {
  return [
    transacaoPenal(c),
    suspensaoProcesso(c),
    anpp(c),
    substituicaoPRD(c),
    sursisPena(c),
    regimeInicial(c),
    progressao(c),
    livramento(c),
    prescricao(c),
    saidaTemporaria(c),
    detracao(),
    remicao(),
    indulto(c),
  ];
}

export const CATEGORIA_LABEL: Record<Categoria, string> = {
  processual: 'Benefícios processuais (pena em abstrato)',
  aplicacao: 'Aplicação da pena (pena concreta)',
  execucao: 'Execução penal',
};

// Benefícios de EXECUÇÃO penal — dependem da pena concreta e do tempo cumprido.
// LEP (Lei 7.210/84), Código Penal e Lei 8.072/90.

import type {BeneficioDef} from '../types';
import {num, bool} from '../types';
import {formatPena, formatFracao} from '../../format';

const ANO = 12;

export const progressao: BeneficioDef = {
  id: 'progressao',
  nome: 'Progressão de regime',
  fundamento: 'Art. 112, LEP (redação da Lei 13.964/2019)',
  categoria: 'execucao',
  natureza: 'concreto',
  descricao:
    'Transferência para regime menos rigoroso após o cumprimento de percentual da pena, ' +
    'somado ao requisito subjetivo de boa conduta carcerária. O Pacote Anticrime ' +
    'substituiu as antigas frações (1/6, 2/5, 3/5) por oito percentuais escalonados.',
  requisitos: [
    'Cumprimento do percentual da pena correspondente ao inciso aplicável (art. 112, I a VIII).',
    'Boa conduta carcerária, comprovada pelo diretor do estabelecimento (art. 112, §1º).',
    'Nos crimes contra a administração pública: reparação do dano ou devolução do produto do ilícito (art. 33, §4º, CP).',
  ],
  vedacoes: [
    'Súmula Vinculante 26, STF: veda a progressão automática; exige exame criminológico quando fundamentado.',
    'Súmula 491, STJ: é inadmissível a progressão per saltum.',
    'Falta grave interrompe o prazo, reiniciando a contagem (Súmula 534, STJ).',
  ],
  parametros: [
    {
      id: 'fracaoPrimarioSemViolencia',
      rotulo: 'Primário, sem violência/grave ameaça',
      tipo: 'fracao',
      padrao: 0.16,
      min: 0,
      max: 1,
      passo: 0.01,
      ajuda: 'Inciso I: 16% da pena para o apenado primário, crime sem violência à pessoa ou grave ameaça.',
      fundamento: 'Art. 112, I, LEP',
    },
    {
      id: 'fracaoReincidenteSemViolencia',
      rotulo: 'Reincidente, sem violência/grave ameaça',
      tipo: 'fracao',
      padrao: 0.2,
      min: 0,
      max: 1,
      passo: 0.01,
      ajuda: 'Inciso II: 20% da pena para o reincidente em crime sem violência à pessoa ou grave ameaça.',
      fundamento: 'Art. 112, II, LEP',
    },
    {
      id: 'fracaoPrimarioViolencia',
      rotulo: 'Primário, com violência/grave ameaça',
      tipo: 'fracao',
      padrao: 0.25,
      min: 0,
      max: 1,
      passo: 0.01,
      ajuda: 'Inciso III: 25% da pena para o primário em crime cometido com violência à pessoa ou grave ameaça.',
      fundamento: 'Art. 112, III, LEP',
    },
    {
      id: 'fracaoReincidenteViolencia',
      rotulo: 'Reincidente, com violência/grave ameaça',
      tipo: 'fracao',
      padrao: 0.3,
      min: 0,
      max: 1,
      passo: 0.01,
      ajuda: 'Inciso IV: 30% da pena para o reincidente em crime cometido com violência à pessoa ou grave ameaça.',
      fundamento: 'Art. 112, IV, LEP',
    },
    {
      id: 'fracaoPrimarioHediondo',
      rotulo: 'Primário, hediondo/equiparado',
      tipo: 'fracao',
      padrao: 0.4,
      min: 0,
      max: 1,
      passo: 0.01,
      ajuda: 'Inciso V: 40% da pena para o primário condenado por crime hediondo ou equiparado.',
      fundamento: 'Art. 112, V, LEP',
    },
    {
      id: 'fracaoPrimarioHediondoMorte',
      rotulo: 'Primário, hediondo com resultado morte',
      tipo: 'fracao',
      padrao: 0.5,
      min: 0,
      max: 1,
      passo: 0.01,
      ajuda: 'Inciso VI: 50% da pena, vedado o livramento condicional.',
      fundamento: 'Art. 112, VI, "a", LEP',
    },
    {
      id: 'fracaoReincidenteHediondo',
      rotulo: 'Reincidente, hediondo/equiparado',
      tipo: 'fracao',
      padrao: 0.6,
      min: 0,
      max: 1,
      passo: 0.01,
      ajuda: 'Inciso VII: 60% da pena para o reincidente na prática de crime hediondo ou equiparado.',
      fundamento: 'Art. 112, VII, LEP',
    },
    {
      id: 'fracaoReincidenteHediondoMorte',
      rotulo: 'Reincidente, hediondo com resultado morte',
      tipo: 'fracao',
      padrao: 0.7,
      min: 0,
      max: 1,
      passo: 0.01,
      ajuda: 'Inciso VIII: 70% da pena, vedado o livramento condicional.',
      fundamento: 'Art. 112, VIII, LEP',
    },
  ],
  avaliar: (c, p) => {
    const comViolencia = c.violencia || c.graveAmeaca;
    let fracao: number;
    let inciso: string;
    if (c.hediondo && c.resultadoMorte && c.reincidenteEspecifico) {
      fracao = num(p, 'fracaoReincidenteHediondoMorte');
      inciso = 'VIII — reincidente específico, hediondo com resultado morte (livramento vedado)';
    } else if (c.hediondo && c.resultadoMorte) {
      fracao = num(p, 'fracaoPrimarioHediondoMorte');
      inciso = 'VI — primário, hediondo com resultado morte (livramento vedado)';
    } else if (c.hediondo && c.reincidenteEspecifico) {
      fracao = num(p, 'fracaoReincidenteHediondo');
      inciso = 'VII — reincidente, hediondo';
    } else if (c.hediondo) {
      fracao = num(p, 'fracaoPrimarioHediondo');
      inciso = 'V — primário, hediondo/equiparado';
    } else if (comViolencia && c.reincidenteEspecifico) {
      fracao = num(p, 'fracaoReincidenteViolencia');
      inciso = 'IV — reincidente, crime com violência/grave ameaça';
    } else if (comViolencia) {
      fracao = num(p, 'fracaoPrimarioViolencia');
      inciso = 'III — primário, crime com violência/grave ameaça';
    } else if (c.reincidenteEspecifico) {
      fracao = num(p, 'fracaoReincidenteSemViolencia');
      inciso = 'II — reincidente, sem violência/grave ameaça';
    } else {
      fracao = num(p, 'fracaoPrimarioSemViolencia');
      inciso = 'I — primário, sem violência/grave ameaça';
    }
    const tempo = c.penaConcreta * fracao;
    return {
      status: 'cabivel',
      resumo: `Fração de ${(fracao * 100).toFixed(0)}% → ${formatPena(tempo)} de cumprimento.`,
      detalhes: [
        `Percentual aplicável: ${inciso}.`,
        `Tempo necessário sobre a pena de ${formatPena(c.penaConcreta)}: ${formatPena(tempo)}.`,
        'Requisito subjetivo: boa conduta carcerária (art. 112, §1º).',
      ],
    };
  },
};

export const livramento: BeneficioDef = {
  id: 'livramento',
  nome: 'Livramento condicional',
  fundamento: 'Art. 83, CP',
  categoria: 'execucao',
  natureza: 'concreto',
  descricao:
    'Antecipação da liberdade, sob condições e período de prova, após o cumprimento de ' +
    'fração da pena. Pressupõe pena privativa igual ou superior a 2 anos, somadas as ' +
    'penas correspondentes a infrações diversas.',
  requisitos: [
    'Pena privativa de liberdade igual ou superior a 2 anos.',
    'Cumprimento da fração legal conforme primariedade, reincidência e hediondez.',
    'Bom comportamento durante a execução e bom desempenho no trabalho atribuído.',
    'Aptidão para prover a própria subsistência mediante trabalho honesto.',
    'Reparação do dano, salvo efetiva impossibilidade de fazê-lo.',
  ],
  vedacoes: [
    'Reincidência específica em crime hediondo ou equiparado (art. 83, V, CP).',
    'Condenado por hediondo com resultado morte (art. 112, VI, "a" e VIII, LEP — livramento vedado).',
    'Súmula 441, STJ: a falta grave não interrompe o prazo para obtenção do livramento condicional.',
  ],
  parametros: [
    {
      id: 'penaMinimaMeses',
      rotulo: 'Pena mínima para acesso ao benefício',
      tipo: 'meses',
      padrao: 2 * ANO,
      min: 0,
      max: 10 * ANO,
      passo: 1,
      ajuda: 'Pressuposto objetivo: penas abaixo deste patamar não admitem livramento condicional.',
      fundamento: 'Art. 83, caput, CP',
    },
    {
      id: 'fracaoPrimario',
      rotulo: 'Primário, bons antecedentes',
      tipo: 'fracao',
      padrao: 1 / 3,
      min: 0,
      max: 1,
      passo: 1 / 24,
      ajuda: 'Art. 83, I: mais de 1/3 da pena, se não reincidente em crime doloso e com bons antecedentes.',
      fundamento: 'Art. 83, I, CP',
    },
    {
      id: 'fracaoReincidente',
      rotulo: 'Reincidente em crime doloso',
      tipo: 'fracao',
      padrao: 1 / 2,
      min: 0,
      max: 1,
      passo: 1 / 24,
      ajuda: 'Art. 83, II: mais de 1/2 da pena, se reincidente em crime doloso.',
      fundamento: 'Art. 83, II, CP',
    },
    {
      id: 'fracaoHediondo',
      rotulo: 'Hediondo/equiparado',
      tipo: 'fracao',
      padrao: 2 / 3,
      min: 0,
      max: 1,
      passo: 1 / 24,
      ajuda: 'Art. 83, V: mais de 2/3 da pena nos crimes hediondos, prática de tortura, tráfico e terrorismo.',
      fundamento: 'Art. 83, V, CP',
    },
    {
      id: 'vedadoReincidenteHediondo',
      rotulo: 'Vedar ao reincidente específico em hediondo',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'Art. 83, V, parte final: vedação absoluta ao reincidente específico em crimes hediondos ou equiparados.',
      fundamento: 'Art. 83, V, CP',
    },
  ],
  avaliar: (c, p) => {
    const minimo = num(p, 'penaMinimaMeses');
    if (c.penaConcreta < minimo) {
      return {
        status: 'incabivel',
        resumo: `Exige pena privativa igual ou superior a ${formatPena(minimo)}.`,
        detalhes: [`Pressuposto objetivo: pena privativa de liberdade igual ou superior a ${formatPena(minimo)}.`],
        limiar: {
          descricao: `Pena concreta ≥ ${formatPena(minimo)}`,
          referenciaMeses: c.penaConcreta,
          limiarMeses: minimo,
          folgaMeses: c.penaConcreta - minimo,
        },
      };
    }
    if (c.hediondo && c.reincidenteEspecifico && bool(p, 'vedadoReincidenteHediondo')) {
      return {
        status: 'incabivel',
        resumo: 'Vedado ao reincidente específico em crime hediondo.',
        detalhes: ['Art. 83, V, CP: vedado para reincidente específico em crimes hediondos ou equiparados.'],
      };
    }
    let fracao: number;
    let base: string;
    if (c.hediondo) {
      fracao = num(p, 'fracaoHediondo');
      base = `crime hediondo/equiparado (${formatFracao(num(p, 'fracaoHediondo'))})`;
    } else if (c.reincidenteEspecifico) {
      fracao = num(p, 'fracaoReincidente');
      base = `reincidente em crime doloso (${formatFracao(num(p, 'fracaoReincidente'))})`;
    } else {
      fracao = num(p, 'fracaoPrimario');
      base = `primário e bons antecedentes (${formatFracao(num(p, 'fracaoPrimario'))})`;
    }
    const tempo = c.penaConcreta * fracao;
    return {
      status: 'cabivel',
      resumo: `Fração de ${formatFracao(fracao)} → ${formatPena(tempo)} cumpridos.`,
      detalhes: [
        `Fração aplicável: ${base}.`,
        `Tempo mínimo de cumprimento: ${formatPena(tempo)}.`,
        'Requisitos: bom comportamento, aptidão para o trabalho e reparação do dano (salvo impossibilidade).',
      ],
    };
  },
};

export const prescricao: BeneficioDef = {
  id: 'prescricao',
  nome: 'Prescrição da pretensão punitiva',
  fundamento: 'Art. 109, CP',
  categoria: 'execucao',
  natureza: 'abstrato',
  descricao:
    'Perda do direito de punir pelo decurso do tempo. Antes do trânsito em julgado, ' +
    'regula-se pelo máximo da pena cominada; depois, pela pena concreta aplicada ' +
    '(art. 110).',
  requisitos: [
    'Decurso do prazo do art. 109, contado conforme o art. 111 (termos iniciais).',
    'Ausência de causas interruptivas (art. 117) ou suspensivas (art. 116) no período.',
  ],
  vedacoes: [
    'Imprescritibilidade constitucional: racismo (art. 5º, XLII, CF) e ação de grupos armados contra a ordem constitucional (art. 5º, XLIV, CF).',
    'Art. 110, §1º: a prescrição retroativa não pode ter por termo inicial data anterior à denúncia.',
  ],
  parametros: [
    {
      id: 'prazoMaisDe12Anos',
      rotulo: 'Pena máx. > 12 anos → prazo',
      tipo: 'meses',
      padrao: 20 * ANO,
      min: 0,
      max: 40 * ANO,
      passo: 12,
      ajuda: 'Art. 109, I: prescreve em 20 anos, se o máximo da pena é superior a 12.',
      fundamento: 'Art. 109, I, CP',
    },
    {
      id: 'prazoMaisDe8Anos',
      rotulo: 'Pena máx. > 8 e ≤ 12 anos → prazo',
      tipo: 'meses',
      padrao: 16 * ANO,
      min: 0,
      max: 40 * ANO,
      passo: 12,
      ajuda: 'Art. 109, II: prescreve em 16 anos, se o máximo da pena é superior a 8 e não excede 12.',
      fundamento: 'Art. 109, II, CP',
    },
    {
      id: 'prazoMaisDe4Anos',
      rotulo: 'Pena máx. > 4 e ≤ 8 anos → prazo',
      tipo: 'meses',
      padrao: 12 * ANO,
      min: 0,
      max: 40 * ANO,
      passo: 12,
      ajuda: 'Art. 109, III: prescreve em 12 anos, se o máximo da pena é superior a 4 e não excede 8.',
      fundamento: 'Art. 109, III, CP',
    },
    {
      id: 'prazoMaisDe2Anos',
      rotulo: 'Pena máx. > 2 e ≤ 4 anos → prazo',
      tipo: 'meses',
      padrao: 8 * ANO,
      min: 0,
      max: 40 * ANO,
      passo: 12,
      ajuda: 'Art. 109, IV: prescreve em 8 anos, se o máximo da pena é superior a 2 e não excede 4.',
      fundamento: 'Art. 109, IV, CP',
    },
    {
      id: 'prazoMaisDe1Ano',
      rotulo: 'Pena máx. ≥ 1 e ≤ 2 anos → prazo',
      tipo: 'meses',
      padrao: 4 * ANO,
      min: 0,
      max: 40 * ANO,
      passo: 12,
      ajuda: 'Art. 109, V: prescreve em 4 anos, se o máximo da pena é igual a 1 ano ou, sendo superior, não excede a 2.',
      fundamento: 'Art. 109, V, CP',
    },
    {
      id: 'prazoAteUmAno',
      rotulo: 'Pena máx. < 1 ano → prazo',
      tipo: 'meses',
      padrao: 3 * ANO,
      min: 0,
      max: 40 * ANO,
      passo: 12,
      ajuda: 'Art. 109, VI: prescreve em 3 anos, se o máximo da pena é inferior a 1 ano (redação da Lei 12.234/2010).',
      fundamento: 'Art. 109, VI, CP',
    },
    {
      id: 'reducaoEtaria',
      rotulo: 'Reduzir pela metade (menor de 21 / maior de 70)',
      tipo: 'booleano',
      padrao: false,
      ajuda: 'Art. 115: prazos reduzidos de metade quando o agente era, ao tempo do crime, menor de 21 anos, ou maior de 70 na data da sentença.',
      fundamento: 'Art. 115, CP',
    },
  ],
  avaliar: (c, p) => {
    const fator = bool(p, 'reducaoEtaria') ? 0.5 : 1;
    const prazo = (penaMeses: number): number => {
      let base: number;
      if (penaMeses > 12 * ANO) base = num(p, 'prazoMaisDe12Anos');
      else if (penaMeses > 8 * ANO) base = num(p, 'prazoMaisDe8Anos');
      else if (penaMeses > 4 * ANO) base = num(p, 'prazoMaisDe4Anos');
      else if (penaMeses > 2 * ANO) base = num(p, 'prazoMaisDe2Anos');
      else if (penaMeses >= 1 * ANO) base = num(p, 'prazoMaisDe1Ano');
      else base = num(p, 'prazoAteUmAno');
      return base * fator;
    };
    const abstrata = prazo(c.penaMax);
    const concreta = c.penaConcreta > 0 ? prazo(c.penaConcreta) : null;
    return {
      status: 'cabivel',
      resumo: `Em abstrato (pena máx.): ${formatPena(abstrata)}.`,
      detalhes: [
        `Prescrição em abstrato, pela pena máxima de ${formatPena(c.penaMax)}: ${formatPena(abstrata)}.`,
        concreta
          ? `Prescrição pela pena concreta de ${formatPena(c.penaConcreta)}: ${formatPena(concreta)}.`
          : 'Informe uma pena concreta para calcular a prescrição retroativa/executória.',
        fator === 0.5
          ? 'Redução do art. 115 APLICADA (menor de 21 no fato ou maior de 70 na sentença).'
          : 'Redução pela metade se o agente é menor de 21 na data do fato ou maior de 70 na sentença (art. 115).',
      ],
    };
  },
};

export const saidaTemporaria: BeneficioDef = {
  id: 'saida-temporaria',
  nome: 'Saída temporária',
  fundamento: 'Art. 122, LEP',
  categoria: 'execucao',
  natureza: 'concreto',
  descricao:
    'Autorização para o condenado em regime semiaberto ausentar-se do estabelecimento ' +
    'sem vigilância direta, para visita à família, frequência a curso ou atividades de ' +
    'ressocialização. A Lei 14.843/2024 restringiu significativamente suas hipóteses.',
  requisitos: [
    'Cumprimento de 1/6 da pena, se primário, ou 1/4, se reincidente (art. 123, II).',
    'Comportamento adequado (art. 123, I).',
    'Compatibilidade do benefício com os objetivos da pena (art. 123, III).',
    'Exclusividade do regime semiaberto.',
  ],
  vedacoes: [
    'Condenado por crime hediondo com resultado morte (art. 122, §2º, com a redação da Lei 14.843/2024).',
    'Saída para participação em atividades de ressocialização foi restringida pela Lei 14.843/2024.',
  ],
  parametros: [
    {
      id: 'fracaoPrimario',
      rotulo: 'Fração — primário',
      tipo: 'fracao',
      padrao: 1 / 6,
      min: 0,
      max: 1,
      passo: 1 / 24,
      ajuda: 'Art. 123, II: cumprimento mínimo de 1/6 da pena para o condenado primário.',
      fundamento: 'Art. 123, II, LEP',
    },
    {
      id: 'fracaoReincidente',
      rotulo: 'Fração — reincidente',
      tipo: 'fracao',
      padrao: 1 / 4,
      min: 0,
      max: 1,
      passo: 1 / 24,
      ajuda: 'Art. 123, II: cumprimento mínimo de 1/4 da pena para o condenado reincidente.',
      fundamento: 'Art. 123, II, LEP',
    },
    {
      id: 'vedadoHediondoMorte',
      rotulo: 'Vedar em hediondo com resultado morte',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'Vedação introduzida pela Lei 14.843/2024 no art. 122, §2º, da LEP.',
      fundamento: 'Art. 122, §2º, LEP (Lei 14.843/2024)',
    },
  ],
  avaliar: (c, p) => {
    const vedado = bool(p, 'vedadoHediondoMorte') && c.hediondo && c.resultadoMorte;
    const fracao = c.reincidenteEspecifico ? num(p, 'fracaoReincidente') : num(p, 'fracaoPrimario');
    const tempo = c.penaConcreta * fracao;
    return {
      status: vedado ? 'incabivel' : 'condicional',
      resumo: vedado
        ? 'Vedada ao condenado por crime hediondo com resultado morte (Lei 14.843/2024).'
        : `Regime semiaberto após ${formatFracao(fracao)} da pena (${formatPena(tempo)}).`,
      detalhes: [
        'Exclusiva do regime semiaberto.',
        `Cumprimento mínimo: ${formatFracao(fracao)} da pena (${c.reincidenteEspecifico ? 'reincidente' : 'primário'}) → ${formatPena(tempo)}.`,
        'Depende de comportamento adequado e compatibilidade com os objetivos da pena.',
        'A Lei 14.843/2024 vedou a saída temporária ao condenado por crime hediondo com resultado morte.',
      ],
    };
  },
};

export const detracao: BeneficioDef = {
  id: 'detracao',
  nome: 'Detração penal',
  fundamento: 'Art. 42, CP',
  categoria: 'execucao',
  natureza: 'incondicionado',
  descricao:
    'Cômputo, na pena privativa de liberdade e na medida de segurança, do tempo de ' +
    'prisão provisória, de prisão administrativa e de internação em hospital de ' +
    'custódia. É direito subjetivo do condenado, aplicável a qualquer tipo penal.',
  requisitos: [
    'Existência de prisão provisória, administrativa ou internação anterior.',
    'Correlação entre a prisão provisória e o processo em que se executa a pena (ou processos conexos).',
  ],
  vedacoes: [
    'Não se admite detração em processo cujo fato seja POSTERIOR à prisão provisória (evita a "conta corrente" de crédito penal).',
  ],
  parametros: [
    {
      id: 'aplicaMedidaSeguranca',
      rotulo: 'Aplicar também à medida de segurança',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'O art. 42 estende expressamente a detração ao tempo de internação em hospital de custódia e tratamento psiquiátrico.',
      fundamento: 'Art. 42, CP',
    },
  ],
  avaliar: (c, p) => ({
    status: 'cabivel',
    resumo: 'Desconto do tempo de prisão provisória/internação.',
    detalhes: [
      'Computa-se na pena privativa e na medida de segurança o tempo de prisão provisória, administrativa ou internação.',
      'Aplicável a qualquer tipo penal; independe da quantidade de pena.',
      bool(p, 'aplicaMedidaSeguranca')
        ? 'Alcança também o tempo de internação em hospital de custódia e tratamento psiquiátrico.'
        : 'Restrito à pena privativa de liberdade (simulação: exclui a medida de segurança).',
      'A detração pode antecipar a data-base da progressão e do livramento condicional.',
    ],
  }),
};

export const remicao: BeneficioDef = {
  id: 'remicao',
  nome: 'Remição de pena',
  fundamento: 'Art. 126, LEP',
  categoria: 'execucao',
  natureza: 'incondicionado',
  descricao:
    'Desconto de dias de pena pelo trabalho ou pelo estudo durante a execução. O tempo ' +
    'remido é computado como pena cumprida para todos os efeitos (art. 128).',
  requisitos: [
    'Cumprimento de pena em regime fechado ou semiaberto (trabalho) ou em qualquer regime (estudo).',
    'Frequência e jornada comprovadas pela administração penitenciária.',
  ],
  vedacoes: [
    'Falta grave: o juiz PODE revogar até 1/3 do tempo remido (art. 127, LEP; Súmula Vinculante 9, STF).',
    'Trabalho: não se admite remição no regime aberto (apenas pelo estudo).',
  ],
  parametros: [
    {
      id: 'diasTrabalhadosPorDiaRemido',
      rotulo: 'Dias trabalhados por 1 dia remido',
      tipo: 'inteiro',
      padrao: 3,
      min: 1,
      max: 10,
      passo: 1,
      ajuda: 'Art. 126, §1º, II: 1 dia de pena a cada 3 dias de trabalho (jornada de 6 a 8 horas).',
      fundamento: 'Art. 126, §1º, II, LEP',
    },
    {
      id: 'horasEstudoPorDiaRemido',
      rotulo: 'Horas de estudo por 1 dia remido',
      tipo: 'inteiro',
      padrao: 12,
      min: 1,
      max: 48,
      passo: 1,
      ajuda: 'Art. 126, §1º, I: 1 dia de pena a cada 12 horas de frequência escolar, divididas em no mínimo 3 dias.',
      fundamento: 'Art. 126, §1º, I, LEP',
    },
    {
      id: 'acrescimoConclusaoCurso',
      rotulo: 'Acréscimo por conclusão de curso',
      tipo: 'fracao',
      padrao: 1 / 3,
      min: 0,
      max: 1,
      passo: 1 / 24,
      ajuda: 'Art. 126, §5º: o tempo remido será acrescido de 1/3 com a conclusão do ensino fundamental, médio ou superior.',
      fundamento: 'Art. 126, §5º, LEP',
    },
  ],
  avaliar: (c, p) => ({
    status: 'cabivel',
    resumo: `Trabalho (1 dia/${num(p, 'diasTrabalhadosPorDiaRemido')}) e estudo (1 dia/${num(p, 'horasEstudoPorDiaRemido')}h).`,
    detalhes: [
      `Trabalho: 1 dia de pena remido a cada ${num(p, 'diasTrabalhadosPorDiaRemido')} dias trabalhados (regime fechado e semiaberto).`,
      `Estudo: 1 dia de pena remido a cada ${num(p, 'horasEstudoPorDiaRemido')} horas de frequência escolar (qualquer regime).`,
      `Conclusão de curso: acréscimo de ${formatFracao(num(p, 'acrescimoConclusaoCurso'))} sobre o tempo remido (art. 126, §5º).`,
      'Aplicável a qualquer tipo penal.',
    ],
  }),
};

export const prisaoDomiciliar: BeneficioDef = {
  id: 'prisao-domiciliar',
  nome: 'Prisão domiciliar',
  fundamento: 'Art. 117, LEP; art. 318, CPP',
  categoria: 'execucao',
  natureza: 'concreto',
  descricao:
    'Recolhimento em residência particular. Na execução (art. 117, LEP), é restrita ao ' +
    'regime aberto em hipóteses humanitárias; no processo (art. 318, CPP), substitui a ' +
    'prisão preventiva. O STF (HC 143.641) a estendeu coletivamente a gestantes e mães ' +
    'de crianças até 12 anos.',
  requisitos: [
    'Execução (art. 117, LEP): regime aberto e uma das hipóteses — maior de 70 anos, acometido de doença grave, com filho menor ou deficiente, ou gestante.',
    'Processo (art. 318, CPP): substituição da preventiva para gestante, mãe/pai de criança até 12 anos, maior de 80 anos, doença grave ou imprescindível aos cuidados de menor de 6 anos.',
  ],
  vedacoes: [
    'HC 143.641/SP, STF: não se estende a crimes cometidos com violência ou grave ameaça, contra os próprios descendentes, ou em situações excepcionalíssimas devidamente fundamentadas.',
  ],
  parametros: [
    {
      id: 'somenteRegimeAberto',
      rotulo: 'Restringir ao regime aberto (execução)',
      tipo: 'booleano',
      padrao: true,
      ajuda:
        'Art. 117 da LEP admite a domiciliar apenas no regime aberto. Desmarcar simula a ' +
        'jurisprudência que a defere por falta de vaga em regime adequado (Súmula Vinculante 56).',
      fundamento: 'Art. 117, LEP; Súmula Vinculante 56, STF',
    },
    {
      id: 'vedadoViolencia',
      rotulo: 'Vedar em crime com violência ou grave ameaça',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'Ressalva do HC 143.641/SP para a domiciliar de gestantes e mães.',
      fundamento: 'HC 143.641/SP, STF',
    },
  ],
  avaliar: (c, p) => {
    const vedado = bool(p, 'vedadoViolencia') && (c.violencia || c.graveAmeaca);
    return {
      status: vedado ? 'incabivel' : 'condicional',
      resumo: vedado
        ? 'Crime com violência ou grave ameaça — ressalva do HC 143.641/SP.'
        : 'Depende de hipótese humanitária (idade, saúde, filho menor ou gestação).',
      detalhes: [
        bool(p, 'somenteRegimeAberto')
          ? 'Execução: restrita ao regime aberto (art. 117, LEP).'
          : 'Restrição de regime DESATIVADA: considera a domiciliar por falta de vaga (Súmula Vinculante 56).',
        'Hipóteses do art. 117, LEP: maior de 70 anos, doença grave, filho menor ou deficiente, gestante.',
        'Processo: art. 318, CPP, substitui a prisão preventiva em hipóteses humanitárias.',
        'HC 143.641/SP, STF: domiciliar coletiva para gestantes e mães de crianças até 12 anos, salvo crime com violência/grave ameaça ou contra descendentes.',
      ],
    };
  },
};

export const monitoracaoEletronica: BeneficioDef = {
  id: 'monitoracao-eletronica',
  nome: 'Monitoração eletrônica',
  fundamento: 'Art. 146-B, LEP; art. 319, IX, CPP',
  categoria: 'execucao',
  natureza: 'concreto',
  descricao:
    'Fiscalização por meio eletrônico. Na execução, acompanha a saída temporária no ' +
    'regime semiaberto e a prisão domiciliar; no processo, é medida cautelar diversa ' +
    'da prisão.',
  requisitos: [
    'Execução (art. 146-B, LEP): autorização de saída temporária no regime semiaberto ou prisão domiciliar.',
    'Processo (art. 319, IX, CPP): medida cautelar diversa da prisão, isolada ou cumulada.',
    'Consentimento e cuidados com o equipamento (art. 146-C, LEP).',
  ],
  vedacoes: [
    'A violação dos deveres do art. 146-C pode acarretar regressão de regime, revogação da saída ou da domiciliar.',
  ],
  parametros: [
    {
      id: 'admiteComoCautelar',
      rotulo: 'Admitir como cautelar diversa da prisão',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'Art. 319, IX, do CPP: monitoração como alternativa à preventiva, aplicável a qualquer tipo penal.',
      fundamento: 'Art. 319, IX, CPP',
    },
    {
      id: 'vedadoHediondo',
      rotulo: 'Vedar em crime hediondo',
      tipo: 'booleano',
      padrao: false,
      ajuda:
        'Não há vedação legal por hediondez. O parâmetro existe para simular propostas ' +
        'legislativas que a introduzam.',
    },
  ],
  avaliar: (c, p) => {
    const vedado = bool(p, 'vedadoHediondo') && c.hediondo;
    return {
      status: vedado ? 'incabivel' : 'condicional',
      resumo: vedado
        ? 'Vedada em crime hediondo (parâmetro de simulação — não há vedação legal vigente).'
        : 'Acompanha a saída temporária, a domiciliar ou substitui a preventiva.',
      detalhes: [
        'Execução: aplicável na saída temporária (regime semiaberto) e na prisão domiciliar (art. 146-B, LEP).',
        bool(p, 'admiteComoCautelar')
          ? 'Processo: medida cautelar diversa da prisão (art. 319, IX, CPP), aplicável a qualquer tipo penal.'
          : 'Uso como cautelar processual DESATIVADO nesta simulação.',
        'Deveres do monitorado: receber visitas, atender contatos e cuidar do equipamento (art. 146-C, LEP).',
        'Não há, na legislação vigente, vedação de monitoração por hediondez.',
      ],
    };
  },
};

export const indulto: BeneficioDef = {
  id: 'indulto',
  nome: 'Indulto coletivo',
  fundamento: 'Art. 84, XII, CF; art. 107, II, CP',
  categoria: 'execucao',
  natureza: 'concreto',
  descricao:
    'Ato de clemência do Presidente da República que extingue a punibilidade de um grupo ' +
    'indeterminado de condenados, por decreto anual. O STF (ADI 5.874) reconheceu ampla ' +
    'discricionariedade do chefe do Executivo na sua concessão.',
  requisitos: [
    'Decreto presidencial vigente que contemple a hipótese.',
    'Cumprimento da fração de pena exigida pelo decreto do ano.',
    'Requisitos subjetivos definidos no decreto (comportamento, ausência de falta grave).',
  ],
  vedacoes: [
    'Art. 5º, XLIII, CF: crimes hediondos, tortura, tráfico ilícito de entorpecentes e terrorismo são insuscetíveis de graça ou anistia.',
    'Os decretos anuais costumam excluir também crimes contra a administração pública e organizações criminosas.',
  ],
  parametros: [
    {
      id: 'vedadoHediondo',
      rotulo: 'Vedar a hediondos e equiparados',
      tipo: 'booleano',
      padrao: true,
      ajuda:
        'Vedação constitucional do art. 5º, XLIII. Alcança hediondos, tortura, tráfico e ' +
        'terrorismo. Desmarcar simula uma alteração constitucional.',
      fundamento: 'Art. 5º, XLIII, CF',
    },
    {
      id: 'fracaoTipica',
      rotulo: 'Fração de pena típica do decreto',
      tipo: 'fracao',
      padrao: 1 / 3,
      min: 0,
      max: 1,
      passo: 1 / 24,
      ajuda:
        'Os decretos variam a cada ano; 1/3 para primários é a fração historicamente mais ' +
        'comum. Não há patamar legal fixo.',
    },
  ],
  avaliar: (c, p) => {
    const vedado = bool(p, 'vedadoHediondo') && c.hediondo;
    const fracao = num(p, 'fracaoTipica');
    return {
      status: vedado ? 'incabivel' : 'condicional',
      resumo: vedado
        ? 'Vedado a crimes hediondos e equiparados.'
        : `Depende do decreto anual (fração típica: ${formatFracao(fracao)} → ${formatPena(c.penaConcreta * fracao)}).`,
      detalhes: [
        'Concedido por decreto presidencial, com requisitos variáveis a cada ano.',
        'Vedado a crimes hediondos, tortura, tráfico e terrorismo (art. 5º, XLIII, CF).',
        `Fração de referência adotada nesta simulação: ${formatFracao(fracao)} da pena.`,
        'ADI 5.874, STF: ampla discricionariedade do Presidente da República na concessão.',
      ],
    };
  },
};

export const comutacao: BeneficioDef = {
  id: 'comutacao',
  nome: 'Comutação de penas',
  fundamento: 'Art. 84, XII, CF; art. 192, LEP',
  categoria: 'execucao',
  natureza: 'concreto',
  descricao:
    'Indulto parcial: em vez de extinguir a punibilidade, REDUZ a pena remanescente na ' +
    'fração fixada pelo decreto presidencial. Beneficia quem cumpriu parte da pena mas ' +
    'não atingiu os requisitos do indulto pleno.',
  requisitos: [
    'Decreto presidencial vigente que preveja a hipótese de comutação.',
    'Cumprimento da fração mínima de pena definida no decreto.',
    'Requisitos subjetivos do decreto (ausência de falta grave no período fixado).',
  ],
  vedacoes: [
    'Art. 5º, XLIII, CF: mesma vedação do indulto para hediondos e equiparados.',
  ],
  parametros: [
    {
      id: 'vedadoHediondo',
      rotulo: 'Vedar a hediondos e equiparados',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'Vedação constitucional do art. 5º, XLIII, aplicável também ao indulto parcial.',
      fundamento: 'Art. 5º, XLIII, CF',
    },
    {
      id: 'fracaoReducao',
      rotulo: 'Fração de redução da pena remanescente',
      tipo: 'fracao',
      padrao: 1 / 4,
      min: 0,
      max: 1,
      passo: 1 / 24,
      ajuda: 'Percentual de redução típico dos decretos de comutação. Varia a cada ano.',
    },
  ],
  avaliar: (c, p) => {
    const vedado = bool(p, 'vedadoHediondo') && c.hediondo;
    const fr = num(p, 'fracaoReducao');
    return {
      status: vedado ? 'incabivel' : 'condicional',
      resumo: vedado
        ? 'Vedada a crimes hediondos e equiparados.'
        : `Redução de ${formatFracao(fr)} da pena remanescente (${formatPena(c.penaConcreta * fr)} sobre ${formatPena(c.penaConcreta)}).`,
      detalhes: [
        'Indulto parcial: reduz a pena em vez de extingui-la.',
        `Fração de redução adotada nesta simulação: ${formatFracao(fr)}.`,
        'Requisitos definidos no decreto presidencial anual (art. 192, LEP).',
        'Vedada a crimes hediondos, tortura, tráfico e terrorismo (art. 5º, XLIII, CF).',
      ],
    };
  },
};

export const graca: BeneficioDef = {
  id: 'graca',
  nome: 'Graça (indulto individual)',
  fundamento: 'Art. 84, XII, CF; art. 188, LEP',
  categoria: 'execucao',
  natureza: 'concreto',
  descricao:
    'Clemência individual concedida pelo Presidente da República a pessoa determinada, ' +
    'em regra mediante petição do condenado, do Ministério Público, do Conselho ' +
    'Penitenciário ou de autoridade administrativa.',
  requisitos: [
    'Provocação por petição do condenado ou por iniciativa do MP, do Conselho Penitenciário ou da autoridade administrativa (art. 188, LEP).',
    'Parecer do Conselho Penitenciário (art. 189, LEP).',
    'Decisão discricionária do Presidente da República.',
  ],
  vedacoes: [
    'Art. 5º, XLIII, CF: insuscetíveis de graça os crimes hediondos, a tortura, o tráfico e o terrorismo.',
    'Art. 2º, I, Lei 8.072/90: reforça a vedação para hediondos e equiparados.',
  ],
  parametros: [
    {
      id: 'vedadoHediondo',
      rotulo: 'Vedar a hediondos e equiparados',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'Vedação expressa do art. 5º, XLIII, da CF e do art. 2º, I, da Lei 8.072/90.',
      fundamento: 'Art. 5º, XLIII, CF; art. 2º, I, Lei 8.072/90',
    },
  ],
  avaliar: (c, p) => {
    const vedado = bool(p, 'vedadoHediondo') && c.hediondo;
    return {
      status: vedado ? 'incabivel' : 'condicional',
      resumo: vedado
        ? 'Vedada a crimes hediondos e equiparados (art. 5º, XLIII, CF).'
        : 'Clemência individual, discricionária, mediante petição e parecer do Conselho Penitenciário.',
      detalhes: [
        'Concedida a pessoa determinada, diferentemente do indulto coletivo.',
        'Processamento: petição instruída, parecer do Conselho Penitenciário e decisão do Presidente da República (arts. 188 a 192, LEP).',
        'Vedada a crimes hediondos, tortura, tráfico e terrorismo (art. 5º, XLIII, CF).',
      ],
    };
  },
};

export const unificacao: BeneficioDef = {
  id: 'unificacao',
  nome: 'Unificação de penas (limite de cumprimento)',
  fundamento: 'Art. 75, CP',
  categoria: 'execucao',
  natureza: 'concreto',
  descricao:
    'O tempo de cumprimento das penas privativas de liberdade não pode ser superior a ' +
    '40 anos (limite elevado de 30 para 40 pela Lei 13.964/2019). A unificação incide ' +
    'apenas sobre o tempo de cumprimento; os benefícios são calculados sobre a pena ' +
    'total aplicada (Súmula 715, STF).',
  requisitos: [
    'Condenação a penas privativas de liberdade cuja soma ultrapasse o limite legal.',
    'Unificação determinada pelo juízo da execução.',
  ],
  vedacoes: [
    'Súmula 715, STF: a pena unificada NÃO é considerada para a concessão de outros benefícios, como o livramento condicional ou o regime mais favorável.',
    'Sobrevindo nova condenação, faz-se nova unificação, desprezando-se o período já cumprido (art. 75, §2º).',
  ],
  parametros: [
    {
      id: 'limiteAnos',
      rotulo: 'Limite máximo de cumprimento (anos)',
      tipo: 'inteiro',
      padrao: 40,
      min: 1,
      max: 100,
      passo: 1,
      ajuda:
        'Teto do art. 75, elevado de 30 para 40 anos pela Lei 13.964/2019 (Pacote Anticrime). ' +
        'É o parâmetro central do debate sobre penas máximas no Brasil.',
      fundamento: 'Art. 75, caput, CP (Lei 13.964/2019)',
    },
    {
      id: 'aplicaSumula715',
      rotulo: 'Benefícios calculados sobre a pena total (Súmula 715)',
      tipo: 'booleano',
      padrao: true,
      ajuda:
        'Súmula 715, STF: a pena unificada não serve de base para os demais benefícios. ' +
        'Desmarcar simula a tese oposta, em que a unificação repercutiria em progressão e livramento.',
      fundamento: 'Súmula 715, STF',
    },
  ],
  avaliar: (c, p) => {
    const limite = num(p, 'limiteAnos') * ANO;
    const excede = c.penaConcreta > limite;
    return {
      status: 'cabivel',
      resumo: excede
        ? `Pena de ${formatPena(c.penaConcreta)} unificada em ${formatPena(limite)} para cumprimento.`
        : `Pena abaixo do teto de ${formatPena(limite)} — sem unificação.`,
      detalhes: [
        `Limite de cumprimento: ${formatPena(limite)} (art. 75, caput).`,
        excede
          ? `Cumprimento limitado a ${formatPena(limite)}, ainda que a pena aplicada seja de ${formatPena(c.penaConcreta)}.`
          : 'A unificação só incide quando a soma das penas supera o teto legal.',
        bool(p, 'aplicaSumula715')
          ? 'Súmula 715, STF: os demais benefícios (progressão, livramento) são calculados sobre a pena TOTAL aplicada, não sobre a unificada.'
          : 'Simulação: benefícios calculados sobre a pena UNIFICADA (contrária à Súmula 715, STF).',
        'Sobrevindo nova condenação, procede-se a nova unificação (art. 75, §2º).',
      ],
      limiar: {
        descricao: `Pena de cumprimento ≤ ${formatPena(limite)}`,
        referenciaMeses: c.penaConcreta,
        limiarMeses: limite,
        folgaMeses: limite - c.penaConcreta,
      },
    };
  },
};

export const EXECUCAO: BeneficioDef[] = [
  progressao,
  livramento,
  prescricao,
  saidaTemporaria,
  detracao,
  remicao,
  prisaoDomiciliar,
  monitoracaoEletronica,
  indulto,
  comutacao,
  graca,
  unificacao,
];

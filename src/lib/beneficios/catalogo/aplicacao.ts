// Benefícios de APLICAÇÃO da pena — dependem, em regra, da pena CONCRETA
// fixada na sentença. Código Penal.

import type {BeneficioDef} from '../types';
import {num, bool} from '../types';
import {formatPena, formatFracao} from '../../format';

const ANO = 12;

export const substituicaoPRD: BeneficioDef = {
  id: 'substituicao',
  nome: 'Substituição por penas restritivas de direitos',
  fundamento: 'Art. 44, CP',
  categoria: 'aplicacao',
  natureza: 'concreto',
  descricao:
    'Troca da pena privativa de liberdade por restritivas de direitos (prestação de ' +
    'serviços, interdição temporária, limitação de fim de semana, prestação pecuniária ' +
    'ou perda de bens). É o principal instrumento de desencarceramento na fase de aplicação.',
  requisitos: [
    'Pena privativa não superior a 4 anos e crime cometido sem violência ou grave ameaça — ou crime culposo, qualquer que seja a pena.',
    'Réu não reincidente em crime doloso.',
    'Culpabilidade, antecedentes, conduta social e personalidade indicarem suficiência da substituição.',
  ],
  vedacoes: [
    'Reincidência específica em crime doloso (art. 44, §3º, parte final).',
    'Crime doloso cometido com violência ou grave ameaça à pessoa (art. 44, I).',
  ],
  parametros: [
    {
      id: 'limiteConcretaMeses',
      rotulo: 'Teto da pena concreta',
      tipo: 'meses',
      padrao: 4 * ANO,
      min: 0,
      max: 20 * ANO,
      passo: 1,
      ajuda:
        'Pena aplicada na sentença não pode superar este valor (crimes dolosos). Elevá-lo é a ' +
        'medida de desencarceramento de maior impacto agregado sobre o catálogo.',
      fundamento: 'Art. 44, I, CP',
    },
    {
      id: 'exigeSemViolencia',
      rotulo: 'Exigir ausência de violência ou grave ameaça (crime doloso)',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'Requisito do art. 44, I. Não se aplica aos crimes culposos.',
      fundamento: 'Art. 44, I, CP',
    },
    {
      id: 'culposoSemTeto',
      rotulo: 'Crime culposo cabível qualquer que seja a pena',
      tipo: 'booleano',
      padrao: true,
      ajuda:
        'Parte final do art. 44, I: nos crimes culposos a substituição independe do quantum ' +
        'da pena aplicada e da existência de violência.',
      fundamento: 'Art. 44, I, parte final, CP',
    },
    {
      id: 'vedadoReincidenteEspecifico',
      rotulo: 'Vedar ao reincidente específico',
      tipo: 'booleano',
      padrao: true,
      ajuda:
        'Art. 44, §3º: o reincidente NÃO específico pode ser beneficiado se a medida for ' +
        'socialmente recomendável; a vedação é absoluta apenas na reincidência específica.',
      fundamento: 'Art. 44, §3º, CP',
    },
  ],
  avaliar: (c, p) => {
    const limite = num(p, 'limiteConcretaMeses');
    const viaCulposo = bool(p, 'culposoSemTeto') && c.culposo;
    const dentroPena = viaCulposo || c.penaConcreta <= limite;
    const semViolencia = viaCulposo || !bool(p, 'exigeSemViolencia') || (!c.violencia && !c.graveAmeaca);
    const naoVedado = !bool(p, 'vedadoReincidenteEspecifico') || !c.reincidenteEspecifico;
    const cabivel = dentroPena && semViolencia && naoVedado;
    return {
      status: cabivel ? 'cabivel' : 'incabivel',
      resumo: !dentroPena
        ? `Pena concreta superior a ${formatPena(limite)}.`
        : !semViolencia
          ? 'Crime doloso com violência ou grave ameaça.'
          : !naoVedado
            ? 'Reincidência específica.'
            : viaCulposo
              ? 'Crime culposo: substituição cabível qualquer que seja a pena.'
              : `Pena concreta ≤ ${formatPena(limite)}, crime sem violência/grave ameaça.`,
      detalhes: [
        `Pena privativa não superior a ${formatPena(limite)} e crime cometido sem violência ou grave ameaça (crime doloso).`,
        'Crimes culposos: cabível qualquer que seja a pena.',
        'Réu não reincidente em crime doloso (reincidente não específico: possível se socialmente recomendável, art. 44, §3º).',
      ],
      limiar: viaCulposo
        ? undefined
        : {
            descricao: `Pena concreta ≤ ${formatPena(limite)}`,
            referenciaMeses: c.penaConcreta,
            limiarMeses: limite,
            folgaMeses: limite - c.penaConcreta,
          },
    };
  },
};

export const sursisPena: BeneficioDef = {
  id: 'sursis-pena',
  nome: 'Suspensão condicional da pena (sursis)',
  fundamento: 'Art. 77, CP',
  categoria: 'aplicacao',
  natureza: 'concreto',
  descricao:
    'Suspensão da execução da pena privativa de liberdade por 2 a 4 anos, mediante ' +
    'condições. É subsidiário: só incide quando incabível a substituição por restritivas ' +
    'de direitos (art. 77, III).',
  requisitos: [
    'Pena privativa de liberdade não superior a 2 anos (sursis comum).',
    'Réu não reincidente em crime doloso.',
    'Circunstâncias do art. 59 autorizarem a concessão.',
    'Não ser indicada ou cabível a substituição por restritivas de direitos.',
  ],
  vedacoes: [
    'Reincidência em crime doloso — salvo se a condenação anterior for exclusivamente de multa (art. 77, §1º).',
  ],
  parametros: [
    {
      id: 'limiteComumMeses',
      rotulo: 'Teto do sursis comum',
      tipo: 'meses',
      padrao: 2 * ANO,
      min: 0,
      max: 10 * ANO,
      passo: 1,
      ajuda: 'Pena concreta máxima para o sursis comum.',
      fundamento: 'Art. 77, caput, CP',
    },
    {
      id: 'limiteEtarioMeses',
      rotulo: 'Teto do sursis etário/humanitário',
      tipo: 'meses',
      padrao: 4 * ANO,
      min: 0,
      max: 10 * ANO,
      passo: 1,
      ajuda: 'Pena concreta máxima para condenado maior de 70 anos ou por razões de saúde.',
      fundamento: 'Art. 77, §2º, CP',
    },
    {
      id: 'vedadoReincidente',
      rotulo: 'Vedar ao reincidente em crime doloso',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'Art. 77, I. A condenação anterior a pena de multa não impede o sursis (§1º).',
      fundamento: 'Art. 77, I e §1º, CP',
    },
  ],
  avaliar: (c, p) => {
    const limite = num(p, 'limiteComumMeses');
    const limiteEtario = num(p, 'limiteEtarioMeses');
    const naoVedado = !bool(p, 'vedadoReincidente') || !c.reincidenteEspecifico;
    const cabivel = c.penaConcreta <= limite && naoVedado;
    const cabivelEtario = c.penaConcreta <= limiteEtario;
    return {
      status: cabivel ? 'cabivel' : cabivelEtario ? 'condicional' : 'incabivel',
      resumo: cabivel
        ? `Pena concreta ≤ ${formatPena(limite)}.`
        : cabivelEtario
          ? `Sursis etário/humanitário: pena ≤ ${formatPena(limiteEtario)} (maior de 70 anos ou por saúde).`
          : 'Pena concreta acima do limite do sursis.',
      detalhes: [
        `Sursis comum: pena privativa não superior a ${formatPena(limite)}, réu não reincidente em crime doloso.`,
        `Sursis etário: pena ≤ ${formatPena(limiteEtario)} para condenado maior de 70 anos.`,
        `Sursis humanitário: pena ≤ ${formatPena(limiteEtario)} por razões de saúde.`,
        'Subsidiário à substituição por PRD (art. 77, III).',
      ],
      limiar: {
        descricao: `Pena concreta ≤ ${formatPena(limite)} (comum)`,
        referenciaMeses: c.penaConcreta,
        limiarMeses: limite,
        folgaMeses: limite - c.penaConcreta,
      },
    };
  },
};

export const regimeInicial: BeneficioDef = {
  id: 'regime',
  nome: 'Regime inicial de cumprimento',
  fundamento: 'Art. 33, §2º e §3º, CP',
  categoria: 'aplicacao',
  natureza: 'concreto',
  descricao:
    'Fixação do regime em que a pena começa a ser cumprida (fechado, semiaberto ou ' +
    'aberto), conforme o quantum da pena, a reincidência e as circunstâncias judiciais.',
  requisitos: [
    'Pena superior a 8 anos: regime inicial fechado.',
    'Pena superior a 4 e até 8 anos: semiaberto, se o condenado não for reincidente.',
    'Pena até 4 anos: aberto, se o condenado não for reincidente.',
  ],
  vedacoes: [
    'Súmula 718, STF: a opinião do julgador sobre a gravidade em abstrato não justifica regime mais severo.',
    'Súmula 719, STF: a imposição de regime mais severo que o previsto exige motivação idônea.',
    'Súmula 440, STJ: fixada a pena-base no mínimo, é vedado o regime mais gravoso pela gravidade abstrata.',
  ],
  parametros: [
    {
      id: 'limiteFechadoMeses',
      rotulo: 'Piso do regime fechado',
      tipo: 'meses',
      padrao: 8 * ANO,
      min: 0,
      max: 40 * ANO,
      passo: 1,
      ajuda: 'Pena concreta ACIMA deste valor impõe regime inicial fechado.',
      fundamento: 'Art. 33, §2º, "a", CP',
    },
    {
      id: 'limiteSemiabertoMeses',
      rotulo: 'Piso do regime semiaberto',
      tipo: 'meses',
      padrao: 4 * ANO,
      min: 0,
      max: 40 * ANO,
      passo: 1,
      ajuda: 'Pena concreta ACIMA deste valor (e até o piso do fechado) impõe semiaberto ao não reincidente.',
      fundamento: 'Art. 33, §2º, "b", CP',
    },
    {
      id: 'hediondoFechado',
      rotulo: 'Hediondo tende ao regime fechado',
      tipo: 'booleano',
      padrao: true,
      ajuda:
        'O STF (HC 111.840) declarou inconstitucional a obrigatoriedade automática do regime ' +
        'inicial fechado nos hediondos; na prática, porém, ele é a regra, com fundamentação. ' +
        'Desmarcar aplica somente os patamares gerais do art. 33.',
      fundamento: 'HC 111.840/ES, STF',
    },
  ],
  avaliar: (c, p) => {
    const pisoFechado = num(p, 'limiteFechadoMeses');
    const pisoSemi = num(p, 'limiteSemiabertoMeses');
    let regime: string;
    if (c.penaConcreta > pisoFechado) regime = 'Fechado';
    else if (c.penaConcreta > pisoSemi) regime = c.reincidenteEspecifico ? 'Fechado' : 'Semiaberto';
    else regime = c.reincidenteEspecifico ? 'Semiaberto' : 'Aberto';

    const detalhes = [
      `Pena superior a ${formatPena(pisoFechado)}: regime inicial fechado.`,
      `Pena superior a ${formatPena(pisoSemi)} e até ${formatPena(pisoFechado)}: semiaberto (não reincidente).`,
      `Pena até ${formatPena(pisoSemi)}: aberto (não reincidente).`,
    ];
    if (c.hediondo && bool(p, 'hediondoFechado')) {
      detalhes.push(
        'Crimes hediondos/equiparados: na prática, regime inicial fechado; o STF (HC 111.840) afastou a obrigatoriedade automática — deve haver fundamentação.',
      );
      regime = c.penaConcreta > pisoSemi ? 'Fechado' : regime;
    }
    return {
      status: 'cabivel',
      resumo: `Regime inicial: ${regime}.`,
      detalhes,
    };
  },
};

export const perdaoJudicial: BeneficioDef = {
  id: 'perdao-judicial',
  nome: 'Perdão judicial',
  fundamento: 'Art. 107, IX, CP',
  categoria: 'aplicacao',
  natureza: 'abstrato',
  descricao:
    'Causa de extinção da punibilidade em que o juiz, nas hipóteses EXPRESSAMENTE ' +
    'previstas em lei, deixa de aplicar a pena. A sentença que o concede não é ' +
    'condenatória e não gera reincidência nem efeitos civis (Súmula 18, STJ).',
  requisitos: [
    'Previsão legal expressa para o tipo penal (não há perdão judicial genérico).',
    'Presença da circunstância eleita pela lei — em regra, consequências da infração que atinjam o próprio agente de forma tão grave que a sanção se torne desnecessária.',
  ],
  vedacoes: [
    'Tipos penais sem previsão expressa: o perdão judicial não pode ser estendido por analogia.',
  ],
  parametros: [
    {
      id: 'somenteCulposos',
      rotulo: 'Restringir às hipóteses culposas',
      tipo: 'booleano',
      padrao: true,
      ajuda:
        'As hipóteses típicas de perdão judicial concentram-se em crimes culposos ' +
        '(homicídio culposo, art. 121, §5º; lesão culposa, art. 129, §8º; receptação ' +
        'culposa, art. 180, §5º). Desmarcar considera também as hipóteses dolosas previstas ' +
        'em lei (ex.: art. 168-A, §3º; art. 4º, Lei 12.850/13).',
      fundamento: 'Art. 121, §5º; art. 129, §8º; art. 180, §5º, CP',
    },
  ],
  avaliar: (c, p) => {
    const restrito = bool(p, 'somenteCulposos');
    const compativel = !restrito || c.culposo;
    return {
      status: compativel ? 'condicional' : 'incabivel',
      resumo: compativel
        ? 'Depende de previsão legal expressa para o tipo penal.'
        : 'Restrito às hipóteses culposas previstas em lei.',
      detalhes: [
        'Só é cabível nas hipóteses expressamente previstas em lei — não existe perdão judicial genérico.',
        'Hipóteses clássicas: homicídio culposo (art. 121, §5º), lesão corporal culposa (art. 129, §8º) e receptação culposa (art. 180, §5º).',
        'Súmula 18, STJ: a sentença concessiva é declaratória da extinção da punibilidade e não subsiste qualquer efeito condenatório.',
        'O catálogo ainda não registra, tipo a tipo, a previsão expressa de perdão judicial — ver roadmap (v1.1.0).',
      ],
    };
  },
};

export const arrependimentoPosterior: BeneficioDef = {
  id: 'arrependimento-posterior',
  nome: 'Arrependimento posterior',
  fundamento: 'Art. 16, CP',
  categoria: 'aplicacao',
  natureza: 'abstrato',
  descricao:
    'Causa obrigatória de diminuição de pena (1/3 a 2/3) quando, nos crimes cometidos ' +
    'sem violência ou grave ameaça, o agente repara o dano ou restitui a coisa por ato ' +
    'voluntário, até o recebimento da denúncia ou da queixa.',
  requisitos: [
    'Crime cometido sem violência ou grave ameaça à pessoa.',
    'Reparação do dano ou restituição da coisa — integral, em regra.',
    'Ato voluntário do agente (não se exige espontaneidade).',
    'Até o recebimento da denúncia ou da queixa.',
  ],
  vedacoes: [
    'Crimes cometidos com violência ou grave ameaça à pessoa.',
    'Reparação posterior ao recebimento da denúncia: incide apenas como atenuante (art. 65, III, "b").',
  ],
  parametros: [
    {
      id: 'fracaoMin',
      rotulo: 'Redução mínima',
      tipo: 'fracao',
      padrao: 1 / 3,
      min: 0,
      max: 1,
      passo: 1 / 24,
      ajuda: 'Piso da causa de diminuição. A fração aproxima-se do máximo quanto mais célere e completa a reparação.',
      fundamento: 'Art. 16, CP',
    },
    {
      id: 'fracaoMax',
      rotulo: 'Redução máxima',
      tipo: 'fracao',
      padrao: 2 / 3,
      min: 0,
      max: 1,
      passo: 1 / 24,
      ajuda: 'Teto da causa de diminuição.',
      fundamento: 'Art. 16, CP',
    },
    {
      id: 'exigeSemViolencia',
      rotulo: 'Exigir ausência de violência ou grave ameaça',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'Requisito expresso do art. 16. Desmarcar simula uma reforma que o estendesse aos crimes violentos.',
      fundamento: 'Art. 16, CP',
    },
    {
      id: 'exigeReparacao',
      rotulo: 'Exigir reparação do dano ou restituição da coisa',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'Sem reparação até o recebimento da denúncia, o benefício não incide.',
      fundamento: 'Art. 16, CP',
    },
  ],
  avaliar: (c, p) => {
    const semViolencia = !bool(p, 'exigeSemViolencia') || (!c.violencia && !c.graveAmeaca);
    const reparou = !bool(p, 'exigeReparacao') || c.reparouDano;
    const frMin = num(p, 'fracaoMin');
    const frMax = num(p, 'fracaoMax');
    const base = c.penaConcreta || c.penaMin;

    let status: 'cabivel' | 'incabivel' | 'condicional';
    let resumo: string;
    if (!semViolencia) {
      status = 'incabivel';
      resumo = 'Crime cometido com violência ou grave ameaça à pessoa.';
    } else if (!reparou) {
      status = 'condicional';
      resumo = 'Cabível se houver reparação do dano até o recebimento da denúncia.';
    } else {
      status = 'cabivel';
      resumo = `Redução de ${formatFracao(frMin)} a ${formatFracao(frMax)} → pena de ${formatPena(base * (1 - frMax))} a ${formatPena(base * (1 - frMin))}.`;
    }
    return {
      status,
      resumo,
      detalhes: [
        'Crime cometido sem violência ou grave ameaça à pessoa.',
        'Reparação do dano ou restituição da coisa, por ato voluntário, até o recebimento da denúncia ou da queixa.',
        `Causa obrigatória de diminuição de ${formatFracao(frMin)} a ${formatFracao(frMax)}; a fração varia conforme a celeridade e a integralidade da reparação.`,
        'Reparação após o recebimento da denúncia: atenuante genérica do art. 65, III, "b".',
      ],
    };
  },
};

export const arrependimentoEficaz: BeneficioDef = {
  id: 'arrependimento-eficaz',
  nome: 'Desistência voluntária e arrependimento eficaz',
  fundamento: 'Art. 15, CP',
  categoria: 'aplicacao',
  natureza: 'abstrato',
  descricao:
    'O agente que voluntariamente desiste de prosseguir na execução, ou impede que o ' +
    'resultado se produza, só responde pelos atos já praticados. Não é causa de ' +
    'diminuição: é exclusão da tipicidade da tentativa (a chamada "ponte de ouro").',
  requisitos: [
    'Iter criminis já iniciado — o tipo deve admitir tentativa.',
    'Desistência voluntária (antes de esgotar os atos executórios) ou arrependimento eficaz (após esgotá-los).',
    'No arrependimento eficaz, a conduta do agente deve efetivamente IMPEDIR o resultado.',
  ],
  vedacoes: [
    'Crimes que não admitem tentativa (unissubsistentes, culposos, omissivos próprios, habituais, preterdolosos).',
    'Resultado consumado apesar do esforço do agente: incide apenas a atenuante do art. 65, III, "b".',
  ],
  parametros: [
    {
      id: 'exigeTentativaAdmitida',
      rotulo: 'Exigir que o tipo admita tentativa',
      tipo: 'booleano',
      padrao: true,
      ajuda:
        'Pressuposto lógico: sem iter criminis fracionável não há execução da qual desistir. ' +
        'Usa o campo "tentativa" do catálogo de tipos penais.',
      fundamento: 'Art. 14, II c/c art. 15, CP',
    },
  ],
  avaliar: (c, p) => {
    const exige = bool(p, 'exigeTentativaAdmitida');
    const compativel = !exige || c.admiteTentativa;
    return {
      status: compativel ? 'condicional' : 'incabivel',
      resumo: compativel
        ? 'Responde só pelos atos já praticados, se a desistência for voluntária ou o resultado for impedido.'
        : 'Tipo não admite tentativa — não há execução da qual desistir.',
      detalhes: [
        'Desistência voluntária: o agente interrompe a execução ainda em curso.',
        'Arrependimento eficaz: esgotados os atos executórios, o agente impede o resultado.',
        'Efeito: exclusão da tipicidade da tentativa — o agente responde apenas pelos atos já praticados.',
        'Se o resultado ocorrer apesar do esforço, resta a atenuante do art. 65, III, "b".',
      ],
    };
  },
};

export const APLICACAO: BeneficioDef[] = [
  substituicaoPRD,
  sursisPena,
  regimeInicial,
  perdaoJudicial,
  arrependimentoPosterior,
  arrependimentoEficaz,
];

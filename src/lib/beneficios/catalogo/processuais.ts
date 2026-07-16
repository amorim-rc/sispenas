// Benefícios processuais — dependem, em regra, da pena em ABSTRATO.
// Lei 9.099/95, CPP e Lei 12.850/13.

import type {BeneficioDef} from '../types';
import {num, bool} from '../types';
import {formatPena, formatFracao} from '../../format';

const ANO = 12;

export const transacaoPenal: BeneficioDef = {
  id: 'transacao',
  nome: 'Transação penal',
  fundamento: 'Art. 76, Lei 9.099/95',
  categoria: 'processual',
  natureza: 'abstrato',
  descricao:
    'Proposta pelo Ministério Público de aplicação imediata de pena restritiva de ' +
    'direitos ou multa, antes do oferecimento da denúncia, nas infrações de menor ' +
    'potencial ofensivo. Não gera reincidência nem efeitos civis.',
  requisitos: [
    'Infração de menor potencial ofensivo (pena máxima não superior a 2 anos, cumulada ou não com multa).',
    'Não ter sido o autor condenado, por sentença definitiva, à pena privativa de liberdade.',
    'Não ter sido beneficiado por transação penal nos 5 anos anteriores.',
    'Antecedentes, conduta social e personalidade favoráveis.',
  ],
  vedacoes: [
    'Violência doméstica e familiar contra a mulher (Súmula 536, STJ; art. 41, Lei 11.340/06).',
    'Concurso de crimes cuja soma das penas máximas ultrapasse o limite legal.',
  ],
  parametros: [
    {
      id: 'limiteMaxMeses',
      rotulo: 'Teto da pena máxima cominada',
      tipo: 'meses',
      padrao: 2 * ANO,
      min: 0,
      max: 20 * ANO,
      passo: 1,
      ajuda:
        'Limite da pena MÁXIMA em abstrato que define a infração de menor potencial ' +
        'ofensivo. Elevá-lo simula uma reforma que ampliasse o alcance dos Juizados Especiais Criminais.',
      fundamento: 'Art. 61, Lei 9.099/95',
    },
    {
      id: 'vedadoViolencia',
      rotulo: 'Vedar quando houver violência ou grave ameaça',
      tipo: 'booleano',
      padrao: true,
      ajuda:
        'A Lei 9.099/95 não veda a transação por violência em geral, mas a Súmula 536 do STJ ' +
        'a afasta na violência doméstica. Desmarcar remove a ressalva e trata esses tipos como cabíveis.',
      fundamento: 'Súmula 536, STJ',
    },
  ],
  avaliar: (c, p) => {
    const limite = num(p, 'limiteMaxMeses');
    const dentroPena = c.penaMax <= limite;
    const ressalva = bool(p, 'vedadoViolencia') && (c.violencia || c.graveAmeaca);
    return {
      status: dentroPena ? (ressalva ? 'condicional' : 'cabivel') : 'incabivel',
      resumo: !dentroPena
        ? `Pena máxima acima de ${formatPena(limite)}.`
        : ressalva
          ? 'Dentro do teto, mas há violência/grave ameaça (ver Súmula 536, STJ).'
          : `Pena máxima ≤ ${formatPena(limite)} → infração de menor potencial ofensivo.`,
      detalhes: [
        `Teto da infração de menor potencial ofensivo: ${formatPena(limite)}.`,
        'Proposta pelo Ministério Público antes do oferecimento da denúncia.',
        'Vedada em casos de violência doméstica e familiar contra a mulher (Súmula 536, STJ).',
      ],
      limiar: {
        descricao: `Pena máxima ≤ ${formatPena(limite)}`,
        referenciaMeses: c.penaMax,
        limiarMeses: limite,
        folgaMeses: limite - c.penaMax,
      },
    };
  },
};

export const suspensaoProcesso: BeneficioDef = {
  id: 'sursis-processual',
  nome: 'Suspensão condicional do processo',
  fundamento: 'Art. 89, Lei 9.099/95',
  categoria: 'processual',
  natureza: 'abstrato',
  descricao:
    'Suspensão do processo por 2 a 4 anos, mediante condições, nos crimes cuja pena ' +
    'mínima cominada não ultrapasse 1 ano. Cumprido o período de prova sem revogação, ' +
    'extingue-se a punibilidade.',
  requisitos: [
    'Pena mínima cominada igual ou inferior a 1 ano.',
    'Acusado não estar sendo processado ou não ter sido condenado por outro crime.',
    'Presentes os demais requisitos do sursis da pena (art. 77, CP).',
  ],
  vedacoes: [
    'Violência doméstica e familiar contra a mulher (Súmula 536, STJ).',
    'Crimes militares (Súmula 9, STM) e infrações do art. 90-A, Lei 9.099/95.',
  ],
  parametros: [
    {
      id: 'limiteMinMeses',
      rotulo: 'Teto da pena mínima cominada',
      tipo: 'meses',
      padrao: 1 * ANO,
      min: 0,
      max: 10 * ANO,
      passo: 1,
      ajuda:
        'Limite da pena MÍNIMA em abstrato. É o patamar mais sensível do sistema: pequenas ' +
        'variações da pena mínima incluem ou excluem faixas inteiras do catálogo.',
      fundamento: 'Art. 89, caput, Lei 9.099/95',
    },
    {
      id: 'periodoProvaMinAnos',
      rotulo: 'Período de prova — mínimo (anos)',
      tipo: 'inteiro',
      padrao: 2,
      min: 1,
      max: 10,
      passo: 1,
      ajuda: 'Prazo mínimo de suspensão do processo, durante o qual o acusado cumpre condições.',
      fundamento: 'Art. 89, caput, Lei 9.099/95',
    },
    {
      id: 'periodoProvaMaxAnos',
      rotulo: 'Período de prova — máximo (anos)',
      tipo: 'inteiro',
      padrao: 4,
      min: 1,
      max: 10,
      passo: 1,
      ajuda: 'Prazo máximo de suspensão do processo.',
      fundamento: 'Art. 89, caput, Lei 9.099/95',
    },
    {
      id: 'vedadoViolencia',
      rotulo: 'Vedar quando houver violência ou grave ameaça',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'Ressalva da Súmula 536 do STJ (violência doméstica). Desmarcar trata esses tipos como cabíveis.',
      fundamento: 'Súmula 536, STJ',
    },
  ],
  avaliar: (c, p) => {
    const limite = num(p, 'limiteMinMeses');
    const dentroPena = c.penaMin <= limite;
    const ressalva = bool(p, 'vedadoViolencia') && (c.violencia || c.graveAmeaca);
    return {
      status: dentroPena ? (ressalva ? 'condicional' : 'cabivel') : 'incabivel',
      resumo: !dentroPena
        ? `Pena mínima acima de ${formatPena(limite)}.`
        : ressalva
          ? 'Dentro do teto, mas há violência/grave ameaça (ver Súmula 536, STJ).'
          : `Pena mínima ≤ ${formatPena(limite)}.`,
      detalhes: [
        `Cabível quando a pena mínima cominada for igual ou inferior a ${formatPena(limite)}.`,
        `Período de prova de ${num(p, 'periodoProvaMinAnos')} a ${num(p, 'periodoProvaMaxAnos')} anos, com condições (art. 89, §1º).`,
        'Vedada em violência doméstica e familiar contra a mulher (Súmula 536, STJ).',
      ],
      limiar: {
        descricao: `Pena mínima ≤ ${formatPena(limite)}`,
        referenciaMeses: c.penaMin,
        limiarMeses: limite,
        folgaMeses: limite - c.penaMin,
      },
    };
  },
};

export const anpp: BeneficioDef = {
  id: 'anpp',
  nome: 'Acordo de não persecução penal (ANPP)',
  fundamento: 'Art. 28-A, CPP',
  categoria: 'processual',
  natureza: 'abstrato',
  descricao:
    'Acordo entre Ministério Público e investigado que confessa formalmente a infração, ' +
    'mediante condições (reparação do dano, renúncia a bens, prestação de serviço, ' +
    'multa). Cumprido o acordo, o juiz declara extinta a punibilidade.',
  requisitos: [
    'Pena mínima cominada inferior a 4 anos.',
    'Infração cometida sem violência ou grave ameaça à pessoa.',
    'Confissão formal e circunstanciada do investigado.',
    'Não ser o caso de arquivamento; acordo necessário e suficiente para reprovação.',
  ],
  vedacoes: [
    'Cabimento de transação penal (art. 28-A, §2º, I).',
    'Investigado reincidente ou com conduta criminal habitual, reiterada ou profissional (§2º, II).',
    'ANPP, transação ou suspensão do processo nos 5 anos anteriores (§2º, III).',
    'Crimes de violência doméstica e familiar contra a mulher ou por razões da condição de sexo feminino (§2º, IV).',
  ],
  parametros: [
    {
      id: 'limiteMinMeses',
      rotulo: 'Teto da pena mínima cominada',
      tipo: 'meses',
      padrao: 4 * ANO,
      min: 0,
      max: 20 * ANO,
      passo: 1,
      ajuda:
        'Pena MÍNIMA em abstrato deve ser INFERIOR a este valor. É o parâmetro central das ' +
        'propostas de ampliação da justiça penal negocial.',
      fundamento: 'Art. 28-A, caput, CPP',
    },
    {
      id: 'exigeSemViolencia',
      rotulo: 'Exigir ausência de violência ou grave ameaça',
      tipo: 'booleano',
      padrao: true,
      ajuda:
        'Requisito do caput do art. 28-A. Desmarcar simula uma reforma que admitisse o ANPP ' +
        'em crimes violentos — mostra a expansão de alcance sobre o catálogo.',
      fundamento: 'Art. 28-A, caput, CPP',
    },
    {
      id: 'exigeConfissao',
      rotulo: 'Exigir confissão formal e circunstanciada',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'Requisito do caput. Sem confissão, o benefício fica condicional (requisitos objetivos atendidos).',
      fundamento: 'Art. 28-A, caput, CPP',
    },
    {
      id: 'vedadoReincidente',
      rotulo: 'Vedar ao reincidente',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'Vedação do art. 28-A, §2º, II (reincidência ou habitualidade criminosa).',
      fundamento: 'Art. 28-A, §2º, II, CPP',
    },
  ],
  avaliar: (c, p) => {
    const limite = num(p, 'limiteMinMeses');
    const dentroPena = c.penaMin < limite;
    const semViolencia = !bool(p, 'exigeSemViolencia') || (!c.violencia && !c.graveAmeaca);
    const naoVedado = !bool(p, 'vedadoReincidente') || !c.reincidenteEspecifico;
    const confissaoOk = !bool(p, 'exigeConfissao') || c.confessou;

    let status: 'cabivel' | 'incabivel' | 'condicional' = 'incabivel';
    let resumo: string;
    if (!dentroPena) {
      resumo = `Pena mínima igual ou superior a ${formatPena(limite)}.`;
    } else if (!semViolencia) {
      resumo = 'Infração praticada com violência ou grave ameaça.';
    } else if (!naoVedado) {
      resumo = 'Vedado ao reincidente (art. 28-A, §2º, II).';
    } else {
      status = confissaoOk ? 'cabivel' : 'condicional';
      resumo = confissaoOk
        ? 'Requisitos objetivos preenchidos.'
        : 'Requisitos objetivos preenchidos; depende de confissão formal.';
    }
    return {
      status,
      resumo,
      detalhes: [
        `Pena mínima inferior a ${formatPena(limite)}.`,
        bool(p, 'exigeSemViolencia')
          ? 'Infração cometida sem violência ou grave ameaça à pessoa.'
          : 'Requisito de ausência de violência DESATIVADO (simulação de reforma).',
        'Confissão formal e circunstanciada do investigado.',
        'Vedado a reincidentes e quando cabível transação penal (art. 28-A, §2º).',
      ],
      limiar: {
        descricao: `Pena mínima < ${formatPena(limite)}`,
        referenciaMeses: c.penaMin,
        limiarMeses: limite,
        folgaMeses: limite - c.penaMin,
      },
    };
  },
};

export const colaboracaoPremiada: BeneficioDef = {
  id: 'colaboracao-premiada',
  nome: 'Colaboração premiada',
  fundamento: 'Art. 4º, Lei 12.850/13',
  categoria: 'processual',
  natureza: 'abstrato',
  descricao:
    'Negócio jurídico processual pelo qual o colaborador que efetiva e voluntariamente ' +
    'auxilia na investigação obtém perdão judicial, redução de até 2/3 da pena privativa ' +
    'de liberdade ou substituição por restritiva de direitos.',
  requisitos: [
    'Colaboração efetiva e voluntária com a investigação e com o processo criminal.',
    'Resultado: identificação de coautores, revelação da estrutura da organização, prevenção de infrações, recuperação de ativos ou localização da vítima com integridade preservada.',
    'Circunstâncias objetivas e subjetivas favoráveis (art. 4º, §1º).',
    'Homologação judicial do acordo (art. 4º, §7º).',
  ],
  vedacoes: [
    'Ausência de voluntariedade — colaboração obtida mediante coação é nula.',
    'O líder da organização e quem ofereceu a proposta primeiro têm tratamento diferenciado para o perdão judicial (art. 4º, §4º).',
  ],
  parametros: [
    {
      id: 'fracaoReducaoMax',
      rotulo: 'Redução máxima da pena',
      tipo: 'fracao',
      padrao: 2 / 3,
      min: 0,
      max: 1,
      passo: 1 / 24,
      ajuda: 'Teto da causa de diminuição para o colaborador (art. 4º, caput).',
      fundamento: 'Art. 4º, caput, Lei 12.850/13',
    },
    {
      id: 'fracaoReducaoPosSentenca',
      rotulo: 'Redução máxima se posterior à sentença',
      tipo: 'fracao',
      padrao: 1 / 2,
      min: 0,
      max: 1,
      passo: 1 / 24,
      ajuda: 'Colaboração posterior à sentença admite redução de até 1/2 ou progressão ainda que ausentes os requisitos objetivos.',
      fundamento: 'Art. 4º, §5º, Lei 12.850/13',
    },
    {
      id: 'admitePerdaoJudicial',
      rotulo: 'Admitir perdão judicial ao colaborador',
      tipo: 'booleano',
      padrao: true,
      ajuda: 'O juiz pode conceder perdão judicial ao colaborador, ainda que não previsto na proposta inicial.',
      fundamento: 'Art. 4º, caput e §2º, Lei 12.850/13',
    },
  ],
  avaliar: (c, p) => {
    const frMax = num(p, 'fracaoReducaoMax');
    const penaBase = c.penaConcreta || c.penaMin;
    const reduzida = penaBase * (1 - frMax);
    return {
      status: 'condicional',
      resumo: `Redução de até ${formatFracao(frMax)}${bool(p, 'admitePerdaoJudicial') ? ' ou perdão judicial' : ''}, conforme a efetividade da colaboração.`,
      detalhes: [
        `Redução de até ${formatFracao(frMax)}: pena de ${formatPena(penaBase)} poderia cair para ${formatPena(reduzida)}.`,
        `Colaboração posterior à sentença: redução de até ${formatFracao(num(p, 'fracaoReducaoPosSentenca'))} (art. 4º, §5º).`,
        'Aplicável a qualquer tipo penal, desde que a colaboração produza um dos resultados do art. 4º, I a V.',
        'Depende de acordo com o Ministério Público ou a autoridade policial e de homologação judicial.',
      ],
    };
  },
};

export const PROCESSUAIS: BeneficioDef[] = [transacaoPenal, suspensaoProcesso, anpp, colaboracaoPremiada];

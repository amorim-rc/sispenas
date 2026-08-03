import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-02-progressao-lei-15358',
  date: '2026-08-02',
  title: 'Progressão de regime: os percentuais dos crimes hediondos estavam desatualizados desde março',
  summary:
    'A Lei 15.358, de março de 2026, reescreveu os percentuais de progressão de regime para crime hediondo — de 40, 50, 60 e 70 por cento para 70, 75, 80 e 85. O sistema seguia calculando pela tabela anterior, e todo resultado de progressão para crime hediondo saía errado. Corrigido.',
  body: [
    'A progressão de regime é calculada por percentual da pena cumprida, e o art. 112 da Lei de Execução Penal fixa qual percentual se aplica a cada situação. Para crime hediondo ou equiparado, a tabela vinha do Pacote Anticrime de 2019: 40 por cento para o primário, 50 para o primário em crime com resultado morte, 60 para o reincidente, 70 para o reincidente em crime com resultado morte.',
    'A Lei 15.358, de 24 de março de 2026, elevou os quatro patamares para 70, 75, 80 e 85 por cento, e acrescentou ao inciso VI uma hipótese nova: o condenado primário por feminicídio, também com livramento condicional vedado. O sistema não havia incorporado a mudança — de modo que, para qualquer crime hediondo, ele informava uma data de progressão mais próxima do que a lei hoje permite.',
    'O erro foi encontrado por uma revisão jurídica das pendências acumuladas, não pela conferência automática: esta compara o catálogo de tipos penais com a lei, e o cálculo de benefícios não estava no seu alcance. É a lacuna mais séria que a revisão apontou, e a primeira a ser fechada.',
    'Os quatro percentuais agora citam a redação vigente e registram, no texto de ajuda, qual era o valor anterior — quem estudar execução penal de fato anterior a março de 2026 precisa saber que a tabela mudou, e que a lei mais benéfica retroage.',
  ],
  tipo: 'correcao',
  areas: ['Benefícios'],
  version: 'v1.7.1',
  links: [
    {
      label: 'Ver os patamares de progressão',
      href: 'https://amorim-rc.github.io/sispenas/docs/beneficios-penais',
    },
  ],
};

export default entrada;

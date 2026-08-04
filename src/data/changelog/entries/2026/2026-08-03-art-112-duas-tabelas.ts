import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-03-art-112-duas-tabelas',
  date: '2026-08-03',
  title: 'A progressão de regime passa a ter duas tabelas, com corte pela data do fato',
  summary:
    'A Lei 15.402, de maio de 2026, reescreveu o caput e os três primeiros incisos do art. 112 da Lei de Execução Penal. Ela não é uniformemente mais benéfica: para o primário condenado por crime sem violência é mais gravosa, e lei mais gravosa não retroage.',
  body: [
    'O caput do art. 112 voltou a fixar patamar próprio — ao menos um sexto da pena no regime anterior — e os incisos passaram a ser exceções a ele, não a lista exaustiva de hipóteses. A expressão é literal: observadas as seguintes exceções.',
    'Disso decorre um efeito que a leitura corrente da lei não capta. Para o apenado primário condenado por crime sem violência ou grave ameaça, o antigo inciso I fixava 16 por cento. Esse inciso foi substituído, e a hipótese passou a cair no caput: um sexto, que é 16,67 por cento. Para esse grupo a lei nova é mais gravosa.',
    'Por isso o sistema passa a ter duas tabelas, e não uma substituição. A retroatividade da lei mais benéfica apura-se por situação concreta, não em bloco. Quem simula um fato anterior a 8 de maio de 2026 marca a circunstância correspondente e recebe o cálculo pela tabela do Pacote Anticrime, que é a lei do caso.',
    'A base de cálculo também mudou, e é o ponto mais consequente. O caput conta um sexto da pena no regime anterior; os incisos contam percentual da pena total. São operações distintas dentro do mesmo artigo. Na primeira progressão as duas bases coincidem, e é ela que o sistema calcula; nas seguintes, a base do caput é o que resta a cumprir.',
    'Os novos incisos I e II ressalvam os crimes contra o Estado Democrático de Direito, e a ressalva é topográfica: basta o crime estar naquele título do Código Penal, sem perguntar se houve violência. Para o primário sobra o caput, por exclusão expressa. Para o reincidente o texto comporta duas leituras sustentáveis, com diferença de 3,33 pontos percentuais, e o sistema devolve o resultado como condicional, com as duas escritas — nenhuma foi escolhida em silêncio.',
    'Implementar isso revelou um defeito antigo no cálculo da dosimetria: a tabela de títulos do Código Penal encerrava o título dos crimes contra a administração pública no art. 359, e os crimes contra o Estado Democrático de Direito, que são artigos 359 com sufixo de letra, caíam ali dentro. Todos recebiam o aumento dos crimes funcionais, que não os alcança. Corrigido.',
  ],
  tipo: 'correcao',
  areas: ['Benefícios', 'Dosimetria'],
  version: 'v1.9.0',
  links: [
    {
      label: 'Ver as duas tabelas de progressão',
      href: 'https://amorim-rc.github.io/sispenas/docs/beneficios-penais',
    },
  ],
};

export default entrada;

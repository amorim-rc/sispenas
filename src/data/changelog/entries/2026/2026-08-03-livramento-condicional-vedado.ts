import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-03-livramento-condicional-vedado',
  date: '2026-08-03',
  title: 'Quatro incisos vedam o livramento condicional, e o sistema só dizia isso por escrito',
  summary:
    'A Lei de Execução Penal proíbe o livramento condicional em quatro situações. O sistema listava as proibições na descrição do benefício, mas seguia calculando o livramento para todas elas: o texto dizia uma coisa e o número dizia outra. Agora a vedação é regra de cálculo.',
  body: [
    'O art. 112 da Lei de Execução Penal fixa quanto da pena precisa ser cumprido para a progressão de regime. Em quatro hipóteses ele acrescenta, na própria letra do inciso, que o livramento condicional fica vedado: o condenado primário por crime hediondo com resultado morte, o reincidente na mesma situação e, desde a Lei 15.358, de março de 2026, quem exerceu comando de organização criminosa ultraviolenta e o primário condenado por feminicídio.',
    'A ficha do livramento condicional já trazia duas dessas vedações escritas. O cálculo, porém, aplicava apenas a vedação do Código Penal, ao reincidente específico em crime hediondo. Resultado: para o condenado por latrocínio, o sistema informava que o livramento seria cabível depois de dois terços da pena, quando a lei o proíbe inteiramente.',
    'As quatro hipóteses passaram a viver numa regra só, com fundamento próprio para cada uma, e com um controle para desligá-la. Quem sustenta que a vedação, por estar em dispositivo de progressão, não alcança o livramento do art. 83 do Código Penal, pode simular essa tese.',
    'Duas hipóteses do inciso VI também não existiam no cálculo da progressão. O comando de organização criminosa ultraviolenta é circunstância do caso, não do tipo, e entrou como caixa de marcação na simulação, ao lado da reincidência; o feminicídio é atributo do tipo e é lido do catálogo. Sem elas, o comandante de facção condenado por crime hediondo sem resultado morte progredia com 70 por cento da pena, quando a lei exige 75 e proíbe o livramento.',
    'Uma pendência ficou registrada e não foi aplicada. Ao conferir o art. 112 no texto oficial, apareceu a Lei 15.402, de maio de 2026, que reescreveu o caput e os três primeiros incisos do artigo, mudança posterior à de março e que o sistema ainda não reflete. Modelá-la exige decidir o que fazer com a duplicação que a própria lei deixou entre dois incisos, e isso é leitura jurídica, não transcrição.',
  ],
  tipo: 'correcao',
  areas: ['Benefícios'],
  version: 'v1.8.0',
  links: [
    {
      label: 'Ver os patamares de progressão e livramento',
      href: 'https://amorim-rc.github.io/sispenas/docs/beneficios-penais',
    },
  ],
};

export default entrada;

import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-31-moldura-autoridade',
  date: '2026-07-31',
  title: 'A pena de cada crime passa a ser definida pelo número, não pelo texto',
  summary:
    'Até aqui, a moldura penal exibida era extraída da observação escrita em cada registro. Uma frase secundária podia mudar a pena publicada — foi o que aconteceu com os maus-tratos contra cão e gato. Agora a moldura vem dos campos numéricos, e a observação voltou a ser apenas descritiva.',
  body: [
    'O catálogo guarda a pena mínima e a máxima em campos próprios, mas quem definia a moldura publicada era o texto da observação, lido por um reconhecedor de padrões. Em 86% dos registros o número era decorativo, e em onze deles os dois se contradiziam. Bastava a observação mencionar outra pena — "antes era três meses a um ano" — para o sistema exibir a faixa errada.',
    'A ordem foi invertida: os campos numéricos são a autoridade, e a observação descreve. Nenhuma pena mudou nesta virada: a moldura de todos os 1.358 tipos permaneceu idêntica, verificada registro a registro. O que melhorou foi a exibição, agora uniforme — "12 anos a 30 anos" passou a "12 a 30 anos", e "12 meses" a "1 ano".',
    'Penas contadas em dias continuam exatas: o mês do art. 11 do Código Penal tem 30 dias, e a conversão foi travada por teste para todo valor de 1 a 29 dias, de modo que "dez dias" nunca vire "9 dias" por arredondamento. A verificação contínua também passou a recusar moldura mal escrita, com mínimo maior que máximo ou número inteiro com casa decimal.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais', 'Dosimetria'],
  version: 'v1.3.0',
  links: [
    {
      label: 'Ver um crime com pena contada em dias',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=504',
    },
  ],
};

export default entrada;

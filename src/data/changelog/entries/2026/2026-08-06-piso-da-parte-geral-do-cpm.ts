import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-06-piso-da-parte-geral-do-cpm',
  date: '2026-08-06',
  title: 'Setenta e oito crimes militares apareciam sem pena mínima',
  summary:
    'O Código Penal Militar comina dezenas de tipos como "reclusão, até seis anos" ou "detenção, até três meses", sem dizer o mínimo. O catálogo publicava esses registros com mínimo zero. O mínimo existe: está no art. 58 da Parte Geral, e vale para todo o Código.',
  body: [
    'O art. 58 do Código Penal Militar diz que o mínimo da pena de reclusão é de um ano e o máximo de trinta anos, e que o mínimo da detenção é de trinta dias e o máximo de dez anos. Quando a cominação do tipo traz só o teto, o piso não é zero nem é ausente: é o da Parte Geral.',
    'A diferença muda benefício. Mínimo zero satisfaz qualquer patamar: o registro entrava como cabível em transação penal, em acordo de não persecução e em suspensão condicional do processo por um piso que a lei não comina. Com o piso corrigido, o furto militar do art. 240 passa de zero a seis anos para um a seis, e o furto de uso do art. 241, de zero a seis meses para trinta dias a seis meses.',
    'A regra vale também para as molduras derivadas de tempo de guerra. O piso do art. 58 integra a moldura do artigo base antes de o fator incidir: o dobro do furto militar parte de dois anos, não de zero. E o teto da reclusão corta o produto quando o dobro o ultrapassa — é o que acontece no roubo e na extorsão de guerra, cujo máximo derivado bate exatamente nos trinta anos do art. 58. Essa regra de corte fica onde está, sem se estender a outros dispositivos.',
    'Foi corrigida junto a espécie de pena dos crimes de guerra que cominam morte no grau máximo: são trinta e seis dispositivos, e trinta e três já constam com a espécie certa. A moldura em meses continua sendo a graduação do art. 81, §2º, que faz a pena de morte corresponder, para esse efeito, à reclusão por trinta anos.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais', 'Benefícios'],
  version: 'v2.0.0',
  links: [
    {
      label: 'Ver o furto militar em tempo de paz',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=700',
    },
  ],
};

export default entrada;

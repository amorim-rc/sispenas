import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-03-causas-de-aumento-e-de-diminuicao',
  date: '2026-08-03',
  title: 'Cento e quatro causas de aumento e de diminuição entram na dosimetria',
  summary:
    'A terceira fase da dosimetria só conhecia as causas de aumento já modeladas uma a uma. Cento e nove dispositivos que a auditoria vinha apontando como ausentes foram conferidos: cento e quatro entraram, e doze foram recusados por não serem causa de aumento nenhuma.',
  body: [
    'A dosimetria pelas três fases usa um catálogo próprio de modificadores: cada agravante, atenuante, causa de aumento e causa de diminuição é um registro com fração, natureza e alcance. A auditoria semanal comparava esse catálogo com o texto das leis e listava o que faltava. Eram cento e nove dispositivos, acumulados havia meses.',
    'Nem tudo o que a lei chama de aumento é causa de aumento. Oito dispositivos do Código de Trânsito estão no capítulo das infrações administrativas: aplicar em dobro a multa por reincidência em doze meses é multa de trânsito, e reincidência administrativa não guarda relação com a reincidência penal. Nada disso entra na dosimetria.',
    'Outros quatro, da Lei de Crimes Ambientais, dizem que se o crime for culposo a pena será reduzida à metade. Isso não é causa de diminuição: a culpa é elemento do tipo, e o que a lei cria é uma modalidade culposa com moldura própria. Registrada como diminuição, a redução seria aplicada depois das demais causas, quando na verdade ela define a moldura de partida. Três viraram tipos penais próprios; o quarto não, porque o artigo a que ele se refere foi vetado.',
    'Nove dispositivos precisaram de dois registros cada, por conterem duas frações ou dois alcances. O mais consequente é o parágrafo 4º do art. 121 do Código Penal: a primeira parte majora o homicídio culposo e a segunda o doloso. Com um registro só, o sistema ofereceria a majorante do homicídio culposo a quem responde por homicídio doloso.',
    'Três formulações não têm mínimo legal: até o dobro, até o triplo, em até um terço. A escolha foi registrar o piso como zero, e ela está documentada porque muda o resultado. Com mínimo zero, a pena majorada pode partir da pena intermediária sem acréscimo, que é o mais favorável ao réu e o único piso que a lei autoriza; inventar um mínimo publicaria como legal um número que a lei não diz.',
  ],
  tipo: 'novidade',
  areas: ['Dosimetria'],
  version: 'v1.8.0',
  links: [
    {
      label: 'Ver a metodologia da dosimetria',
      href: 'https://amorim-rc.github.io/sispenas/docs/metodologia',
    },
  ],
};

export default entrada;

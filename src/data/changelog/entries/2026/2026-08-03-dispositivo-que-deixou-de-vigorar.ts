import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-03-dispositivo-que-deixou-de-vigorar',
  date: '2026-08-03',
  title: 'Um crime militar foi declarado inconstitucional, e continua no catálogo com a data em que deixou de valer',
  summary:
    'O Supremo declarou inconstitucional o estupro de vulnerável do Código Penal Militar, com efeitos a partir de agosto de 2025. Fato anterior a essa data continua regido por ele. O catálogo ganhou campos para dizer desde quando um dispositivo não vale mais, e o que se aplica no lugar.',
  body: [
    'Em agosto de 2025 o Supremo Tribunal Federal julgou inconstitucional o parágrafo 3º do art. 232 do Código Penal Militar, por proteção deficiente: ele punia o estupro de vulnerável praticado por militar com oito a quinze anos, sem agravamento por lesão grave ou morte, enquanto o Código Penal comina dez a vinte e doze a trinta nessas hipóteses. A decisão tem efeitos apenas para o futuro.',
    'Isso cria uma situação que o catálogo não sabia representar. Excluir o registro apagaria a lei que valia quando o fato ocorreu, e uma consulta sobre um fato de 2024 precisa da lei de 2024. Mantê-lo sem dizer nada publicaria como vigente o que o Supremo derrubou.',
    'Os dados abertos ganharam dois campos: a data em que o dispositivo deixou de vigorar e uma nota obrigatória com o que houve e qual dispositivo passa a reger a conduta, aqui o art. 217-A do Código Penal e todos os seus parágrafos, por força da regra que manda aplicar a lei penal comum onde a militar é omissa. Na tela do tipo penal, uma etiqueta mostra a data, e a nota aparece ao passar o mouse.',
    'Na mesma revisão, o tráfico de drogas em lugar sujeito à administração militar deixou de constar como hediondo por identidade. A Lei dos Crimes Hediondos projeta sobre o Código Penal Militar apenas os crimes previstos no seu art. 1º, e o tráfico não está lá: é equiparado por dispositivo diverso. Se a equiparação constitucional alcança o tipo militar é outra pergunta, com consequências que não coincidem, e ficou registrada como pendência.',
    'O critério de identidade adotado passou a constar por escrito ao lado da tabela: correspondência de conduta e bem jurídico com a hipótese específica do rol, não bastando o nome do crime. Se bastasse o nome, todo roubo militar seria hediondo, quando a lei torna hedionda apenas quatro formas do roubo comum. É matéria sem jurisprudência consolidada, e o arquivo diz isso.',
  ],
  tipo: 'novidade',
  areas: ['Tipos penais', 'Interface'],
  version: 'v1.8.0',
  links: [
    {
      label: 'Ver o contrato dos dados abertos',
      href: 'https://amorim-rc.github.io/sispenas/docs/dados-abertos',
    },
  ],
};

export default entrada;

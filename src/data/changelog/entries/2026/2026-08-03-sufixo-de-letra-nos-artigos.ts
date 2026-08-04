import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-03-sufixo-de-letra-nos-artigos',
  date: '2026-08-03',
  title: 'A injúria racial estava colada num artigo vetado, por causa de uma letra',
  summary:
    'Artigos com sufixo de letra, como 2º-A e 359-M-B, não eram reconhecidos em todas as formas pelo leitor de textos legais. O efeito ia de um crime inteiro colado no artigo errado a oitenta e oito artigos que não existem.',
  body: [
    'O sistema lê os textos compilados oficiais e os quebra em dispositivos, para comparar cada um com o catálogo. O reconhecedor de artigo aceitava um sufixo de letra colado ao número, como em 121-A. Faltavam duas formas.',
    'A primeira é o sufixo depois do marcador ordinal, como em 2º-A. O marcador era consumido primeiro, o artigo virava o de número 2 e o resto do identificador ia para dentro do texto. Na Lei de Racismo, o art. 2º está vetado, e a injúria racial inteira aparecia colada nele, inclusive a majorante do parágrafo único, que passou a constar sob um identificador que a lei não tem e que a revisão jurídica precisou levantar à mão.',
    'A segunda é o sufixo duplo, como em 359-M-B. A redução de pena por contexto de multidão aparecia colada ao crime de golpe de Estado, que é outro artigo.',
    'Na direção oposta, o mesmo padrão inventava artigos. Um artigo escrito com hífen de pontuação seguido de artigo definido, como em Art. 13 - O resultado, virava um inexistente Art. 13-O, e o texto passava a começar em resultado. Eram oitenta e oito artigos assim.',
    'Corrigido dos dois lados, no leitor e na função que reduz o artigo do catálogo à mesma chave, porque corrigir só um faz o registro existir e não ser conferido. Quarenta dispositivos que existiam e não eram vistos apareceram, entre eles os arts. 3º-A a 3º-C da Lei de Organizações Criminosas e os arts. 8º-A a 8º-F da Lei de Drogas.',
  ],
  tipo: 'melhoria',
  areas: ['Tipos penais'],
  version: 'v1.8.0',
  links: [
    {
      label: 'Ver como o catálogo é conferido',
      href: 'https://amorim-rc.github.io/sispenas/docs/metodologia',
    },
  ],
};

export default entrada;

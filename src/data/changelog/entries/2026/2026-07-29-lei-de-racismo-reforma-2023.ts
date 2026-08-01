import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-29-lei-de-racismo-reforma-2023',
  date: '2026-07-29',
  title: 'Lei de Racismo alinhada à reforma de 2023, e dois aumentos que eram linhas viram modificadores',
  summary:
    'A Lei 14.532/2023 reformou a Lei de Racismo, e o catálogo tinha dois erros de modelagem: os arts. 20-A e 20-B, que são causas de aumento, constavam como se fossem crimes autônomos. Corrigido no mesmo padrão do Código Penal.',
  body: [
    'Os arts. 20-A (contexto de descontração ou recreação) e 20-B (crime praticado por funcionário público) não descrevem condutas: mandam aumentar de um terço à metade a pena dos crimes de racismo. Deixam de ser linhas do catálogo e passam a modificadores da dosimetria, ao lado do aumento de metade da injúria racial cometida em concurso de pessoas.',
    'Entram também três formas do art. 20 que faltavam: a discriminação por meios de comunicação, redes sociais ou internet (§2º, 2 a 5 anos), em atividades esportivas, religiosas ou culturais (§2º-A, 2 a 5 anos e proibição de frequência), e a violência contra manifestações religiosas (§2º-B, nas mesmas penas do caput).',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais', 'Dosimetria'],
  version: 'v1.2.10',
  links: [
    {
      label: 'Ver a injúria racial e seus aumentos',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=582',
    },
  ],
};

export default entrada;

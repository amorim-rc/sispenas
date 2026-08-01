import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-28-cp-crimes-ausentes-147c-338a',
  date: '2026-07-28',
  title:
    'Dois crimes que faltavam no Código Penal: ameaça em contexto de organização criminosa e descumprimento de medida protetiva',
  summary:
    'A revisão sistemática do Código Penal contra o texto compilado começou e já repôs dois tipos que a lei criou e o catálogo não tinha: o art. 147-C (Lei 15.358/2026) e o art. 338-A (Lei 15.280/2025).',
  body: [
    'O método da revisão é deixar o próprio texto compilado apontar o que mudou: cada dispositivo traz a lei que o incluiu, alterou ou revogou. Cruzando essas anotações com o catálogo, a defasagem aparece sem reler o que está intacto.',
    'O art. 147-C pune a ameaça de mal injusto e grave no contexto de organização criminosa ultraviolenta, com reclusão de 1 a 3 anos. O art. 338-A pune o descumprimento de decisão que defere medidas protetivas de urgência, com reclusão de 2 a 5 anos e multa — figura mais ampla que o art. 24-A da Lei Maria da Penha.',
    'São os primeiros de uma revisão do Código Penal inteiro no mesmo rigor do art. 121: o Código sofreu reforma pesada entre 2023 e 2026, e outras correções virão por lote.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais'],
  version: 'v1.2.2',
  links: [
    {
      label: 'Ver o art. 147-C no catálogo',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=1322',
    },
  ],
};

export default entrada;

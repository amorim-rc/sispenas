import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-28-dosimetria-modificadores-org-criminosa',
  date: '2026-07-28',
  title:
    'Seis novos modificadores de dosimetria — e o motor aprendeu o aumento "em triplo"',
  summary:
    'Fecha a revisão do Código Penal: os aumentos e a diminuição que não são forma autônoma — porque incidem sobre a pena de qualquer forma do crime — entram como modificadores da 3ª fase, e não como linhas do catálogo.',
  body: [
    'São os aumentos por organização criminosa ultraviolenta que mandam elevar a respectiva pena — na lesão corporal (art. 129, §8º-A, +2/3), na extorsão (art. 158, §4º, em triplo), na extorsão mediante sequestro (art. 159, §5º, +2/3) e na receptação (art. 180, §8º, +2/3) —, o aumento de um terço ao dobro nos crimes patrimoniais contra instituições financeiras (art. 183-A) e a redução de um a dois terços por contexto de multidão nos crimes contra as instituições democráticas (art. 359-M-B).',
    'Para isso o cálculo ganhou duas capacidades: oferecer um modificador que incide no próprio artigo do crime sem contá-lo duas vezes, e representar o aumento "em triplo", que multiplica a pena por três — algo que a 3ª fase, antes limitada a frações até a metade, não sabia expressar.',
  ],
  tipo: 'melhoria',
  areas: ['Dosimetria'],
  version: 'v1.2.6',
  links: [
    {
      label: 'Ver os modificadores na extorsão',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=106',
    },
  ],
};

export default entrada;

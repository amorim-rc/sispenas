import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-29-ctb-sinistro-de-transito',
  date: '2026-07-29',
  title: 'CTB: "acidente" passa a "sinistro de trânsito"',
  summary:
    'A triagem do Código de Trânsito Brasileiro não encontrou mudança de pena ou de tipo desde 2023, mas a Lei 14.599/2023 trocou, em toda a lei, "acidente de trânsito" por "sinistro de trânsito". O catálogo foi alinhado ao termo atual.',
  body: [
    'A troca de nomenclatura é uma escolha deliberada do legislador: "sinistro" é neutro quanto à culpa, enquanto "acidente" sugere fatalidade. O crime de fuga do local (art. 305) tinha a descrição atualizada para refletir o termo vigente. Penas e elementos permanecem os mesmos.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais'],
  version: 'v1.2.11',
  links: [
    {
      label: 'Ver a fuga do local do sinistro (art. 305)',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=353',
    },
  ],
};

export default entrada;

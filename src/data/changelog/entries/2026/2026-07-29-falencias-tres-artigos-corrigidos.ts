import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-29-falencias-tres-artigos-corrigidos',
  date: '2026-07-29',
  title: 'Falências: três crimes corrigidos para o que a lei realmente prevê',
  summary:
    'A Lei de Falências (Lei 11.101/2005) não teve reforma penal desde 2023, mas a conferência artigo a artigo contra o texto compilado revelou três registros com crime ou pena trocados.',
  body: [
    'O art. 171 estava descrito como sonegação de bens, quando pune sonegar ou omitir informações no processo de falência ou recuperação (a pena de reclusão de 2 a 4 anos já estava correta). O art. 173, registrado como adulteração de documentos com pena de 3 a 6 anos, na verdade pune a apropriação, o desvio ou a ocultação de bens do devedor ou da massa, com reclusão de 2 a 4 anos.',
    'O art. 177 trazia a omissão de documentos contábeis, com detenção de 1 a 2 anos — que é o crime do art. 178, já presente no catálogo. O art. 177 pune, na verdade, a violação de impedimento: a aquisição de bens da massa pelo juiz, pelo membro do Ministério Público, pelo administrador judicial, pelo perito e por outros agentes do processo, com reclusão de 2 a 4 anos.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais'],
  version: 'v1.2.11',
  links: [
    {
      label: 'Ver a apropriação de bens da massa (art. 173)',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=486',
    },
  ],
};

export default entrada;

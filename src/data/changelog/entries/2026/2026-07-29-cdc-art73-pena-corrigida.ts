import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-29-cdc-art73-pena-corrigida',
  date: '2026-07-29',
  title: 'CDC: pena do art. 73 corrigida de anos para meses',
  summary:
    'A triagem do Código de Defesa do Consumidor não encontrou reforma penal desde 2023, mas revelou um erro de registro: o art. 73 estava com pena de 1 a 5 anos, quando a lei prevê detenção de 1 a 6 meses.',
  body: [
    'O art. 73 pune deixar de corrigir imediatamente informação sobre consumidor, constante de cadastro ou banco de dados, que se sabe inexata. A pena legal é detenção de 1 a 6 meses, ou multa — o catálogo trazia 1 a 5 anos, provável troca de unidade. Corrigido contra o texto compilado. Os demais crimes do CDC (arts. 63 a 74) foram conferidos e conferem.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais'],
  version: 'v1.2.11',
  links: [
    {
      label: 'Ver o art. 73 do CDC',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=515',
    },
  ],
};

export default entrada;

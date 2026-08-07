import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-06-estatuto-da-pessoa-idosa',
  date: '2026-08-06',
  title: 'O Estatuto da Pessoa Idosa passa a usar a nomenclatura vigente em todo o diploma',
  summary:
    'A Lei 14.423/2022 mudou a denominação oficial: "Estatuto do Idoso" deixou de ser o nome da lei. A v1.9.0 aplicou a mudança a dois registros; os sete restantes ficaram para trás. Agora o diploma inteiro está uniforme.',
  body: [
    'O nome do tipo, no catálogo, é rótulo editorial, não transcrição legal — todos já são paráfrase do dispositivo. Construí-lo com a nomenclatura vigente não falseia nada. A linha que não se atravessa é outra: o texto legal transcrito na observação preserva a letra do que a lei diz, e não foi tocado.',
    'Os sete registros passaram, junto, a nomear a conduta em vez de recitá-la: "Deixar de prestar assistência ao idoso quando obrigado por lei" virou "Omissão de socorro à pessoa idosa", e a descrição inteira continua na observação, onde sempre esteve.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais', 'Interface'],
  version: 'v2.0.0',
  links: [
    {
      label: 'Ver a omissão de socorro à pessoa idosa',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=467',
    },
  ],
};

export default entrada;

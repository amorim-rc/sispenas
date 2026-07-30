import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-30-ambiental-molduras-conferidor',
  date: '2026-07-30',
  title: 'Crimes ambientais: três molduras corrigidas — as primeiras achadas pelo conferidor',
  summary:
    'A primeira rodada do conferidor automático encontrou três penas divergentes do texto oficial na Lei de Crimes Ambientais. Uma delas fazia o site publicar "3 meses a 1 ano" para um crime punido com reclusão de 2 a 5 anos.',
  body: [
    'Os maus-tratos contra cão ou gato (art. 32, §1º-A) apareciam com pena de 3 meses a 1 ano. A pena correta é reclusão de 2 a 5 anos, da Lei Sansão. O engano não estava nos números do registro, e sim na observação: ela mencionava a pena antiga ("antes era 3 meses a 1 ano"), e era essa faixa que o sistema lia ao montar a moldura exibida. A menção histórica foi mantida, agora escrita por extenso.',
    'A destruição de florestas nativas (art. 50) constava com 6 meses a 3 anos, quando a lei comina detenção de 3 meses a 1 ano. O laudo ambiental falso (art. 69-A) constava com 3 a 5 anos, quando a lei comina reclusão de 3 a 6 anos.',
    'As três correções foram propostas automaticamente e conferidas contra o texto compilado antes de entrar: o sistema reescreve o registro, recalcula a moldura publicada pelo mesmo caminho que o site usa e descarta a proposta se o resultado não reproduzir a pena da lei.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais'],
  version: 'v1.2.16',
  links: [
    {
      label: 'Ver os maus-tratos contra cão ou gato',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=622',
    },
  ],
};

export default entrada;

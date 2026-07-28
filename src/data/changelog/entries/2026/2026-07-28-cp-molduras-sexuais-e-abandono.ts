import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-28-cp-molduras-sexuais-e-abandono',
  date: '2026-07-28',
  title:
    'Penas atualizadas nos crimes sexuais e no abandono, e três dispositivos que já não existiam',
  summary:
    'Terceiro lote da revisão do Código Penal: as molduras defasadas dos crimes sexuais (Lei 15.280/2025) e do abandono de incapaz e maus-tratos (Lei 15.163/2025) foram corrigidas para a redação atual, e três registros que a lei já não comporta saíram do catálogo.',
  body: [
    'A Lei 15.280/2025 elevou as penas do estupro de vulnerável (art. 217-A, agora 10 a 18 anos no caput, 12 a 24 se há lesão grave, 20 a 40 se há morte) e dos arts. 218, 218-A, 218-B e 218-C. A Lei 15.163/2025 transformou o abandono de incapaz (art. 133) e os maus-tratos (art. 136) de detenção em reclusão, com penas de 2 a 5 anos no caput, 3 a 7 com lesão grave e 8 a 14 com morte.',
    'Saíram três registros: o art. 218, §2º (a antiga corrupção de menores, revogada pela reestruturação de 2009 e que o catálogo ainda listava), o art. 218-B, §1º (revogado pela Lei 15.280/2025) e uma duplicata do art. 218-C que estava rotulada como se fosse do ECA.',
    'A revisão do Código Penal segue por lote, sempre conferindo cada moldura contra o texto compilado oficial.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais'],
  version: 'v1.2.4',
  links: [
    {
      label: 'Ver o estupro de vulnerável no catálogo',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=148',
    },
  ],
};

export default entrada;

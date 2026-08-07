import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-29-agrotoxicos-lei-14785',
  date: '2026-07-29',
  title: 'Agrotóxicos: catálogo migrado da lei revogada para o novo marco (Lei 14.785/2023)',
  summary:
    'A Lei 14.785/2023 revogou a antiga Lei de Agrotóxicos (Lei 7.802/1989) e trouxe novos crimes. O catálogo ainda apontava para a lei revogada; foi migrado para os dispositivos vigentes.',
  body: [
    'O crime de produzir, transportar, importar, utilizar ou comercializar agrotóxicos irregulares deixa de ser o art. 15 da lei antiga (reclusão de 2 a 4 anos) e passa a ser o art. 56 da Lei 14.785/2023, agora exigindo produto não registrado ou não autorizado e com pena maior: reclusão de 3 a 9 anos, e multa.',
    'O art. 56 traz quatro causas de aumento, incorporadas à dosimetria: dano à propriedade alheia (de um sexto a um terço), dano ao meio ambiente (de um terço à metade), lesão corporal grave (da metade a dois terços) e morte (de dois terços até o dobro). Entra também o art. 57 — resíduos e embalagens vazias em desacordo, com reclusão de 2 a 4 anos. A antiga modalidade culposa (art. 16 da lei revogada) não foi reeditada e saiu do catálogo.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais', 'Dosimetria'],
  version: 'v1.2.12',
  links: [
    {
      label: 'Ver o crime de agrotóxico irregular (art. 56)',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=654',
    },
  ],
};

export default entrada;

import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-31-rodada-conferidor',
  date: '2026-07-31',
  title: 'Noventa penas corrigidas contra o texto oficial, em vinte e um diplomas',
  summary:
    'Primeira leva de correções vinda da conferência automática do catálogo contra o texto compilado do Planalto. Noventa molduras penais divergiam da lei — algumas por décadas de diferença — e foram acertadas dispositivo a dispositivo.',
  body: [
    'As correções alcançam vinte e um diplomas, com maior concentração no Código Penal. São penas que estavam registradas fora do que a lei comina: a violência doméstica do art. 129, §9º constava com 3 meses a 3 anos, quando a Lei 14.994/2024 a elevou para reclusão de 2 a 5 anos; o estupro qualificado do art. 213, §1º constava com 6 a 10 anos, quando a lei prevê 8 a 12; os maus-tratos contra cão ou gato apareciam com 3 meses a 1 ano no lugar da reclusão de 2 a 5 anos da Lei Sansão.',
    'Nada foi criado nem removido: cada correção ajusta a moldura ou a espécie de pena de um registro que já existia, e cada uma cita o dispositivo conferido na fonte oficial. Os achados que exigem decisão jurídica — dispositivos ausentes do catálogo, crimes revogados que ainda constam como vigentes e preceitos que cominam duas penas no mesmo texto — ficaram de fora desta leva e seguem para exame caso a caso.',
    'A conferência também recusou o que não soube ler com segurança. Um preceito que comina pena junto de valores em cruzeiros produziu uma faixa invertida, e a verificação a rejeitou em vez de publicar um dado incoerente.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais'],
  version: 'v1.3.0',
  links: [
    {
      label: 'Ver a violência doméstica (art. 129, §9º)',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=61',
    },
  ],
};

export default entrada;

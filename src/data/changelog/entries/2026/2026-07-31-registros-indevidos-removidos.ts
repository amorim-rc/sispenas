import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-31-registros-indevidos-removidos',
  date: '2026-07-31',
  title: 'Trinta e um registros que não eram crimes vigentes saem do catálogo',
  summary:
    'A conferência automática foi virada contra o seu próprio resultado: dos 95 tipos que ela mesma acrescentou ontem, 29 não eram tipos penais vigentes — e mais dois erros antigos apareceram junto. O catálogo passa de 1.449 para 1.418 registros, e cada saída fica registrada no acervo histórico.',
  body: [
    'A maior parte eram redações do Código Penal transcritas dentro das leis que o alteraram. O texto compilado do Planalto reproduz, embaixo do artigo alterador, a redação que ele deu à outra lei: a Lei 8.137 exibe o art. 172 do Código Penal, a Lei Maria da Penha exibe o art. 129, parágrafo 9º, a Lei 12.850 exibe o art. 288. Cada um desses crimes já estava no catálogo, no diploma certo e com a redação de hoje — a transcrição congela a redação da época da alteração, de modo que o registro duplicado nascia, além de duplicado, desatualizado.',
    'Os demais foram quatro contravenções revogadas que mantêm o texto na página oficial, com a revogação anotada ao lado; quatro duplicatas do art. 190 do Código Penal Militar, que apareciam sob o número 189; duas infrações administrativas do Estatuto da Criança e do Adolescente, punidas com multa, em que a suspensão da programação prevista para a reincidência foi lida como pena de prisão; duas normas de equiparação do Código Eleitoral, que dizem o que se considera documento e não descrevem conduta; e três dispositivos sem preceito penal, cuja pena pertencia a outro artigo do mesmo diploma.',
    'Dois erros são anteriores à conferência automática e vinham publicados havia tempo: os arts. 245 e 246 do Estatuto da Criança e do Adolescente constavam com detenção de seis meses a dois anos, quando são infrações administrativas punidas com multa. A pena registrada era, na verdade, a do art. 236, que já tem registro próprio.',
    'Três penas da Lei 6.766/1979 também foram corrigidas: o art. 50, incisos I a III, constava com um a cinco anos de reclusão, quando o texto comina um a quatro; cinco anos é a pena da forma qualificada, do parágrafo único.',
    'Só as quatro contravenções revogadas foram para o acervo histórico, que reúne o que já foi crime no Brasil. Os demais registros não deixaram de ser crime: nunca foram, e por isso não são material de acervo. O que houve com cada um está descrito aqui, nesta nota, que é o registro permanente da mudança.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais', 'Acervo histórico'],
  version: 'v1.4.0',
  links: [
    {
      label: 'Ver os registros retirados',
      href: 'https://amorim-rc.github.io/sispenas/docs/acervo-historico',
    },
  ],
};

export default entrada;

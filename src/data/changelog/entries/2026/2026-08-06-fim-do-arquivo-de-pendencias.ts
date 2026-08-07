import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-06-fim-do-arquivo-de-pendencias',
  date: '2026-08-06',
  title: 'O arquivo de perguntas jurídicas em aberto saiu, porque as perguntas foram respondidas',
  summary:
    'O REVISAO-PENDENTE.md guardava as questões que o projeto examinou e deixou abertas de propósito, para não preencher lacuna com plausibilidade. A revisão da base respondeu as que dependiam do texto legal e aplicou as que já estavam respondidas. O arquivo foi removido, e com ele o bloco de pendências do relatório semanal.',
  body: [
    'O que era pergunta virou dado: a hediondez por identidade no Código Penal Militar, o desdobramento por inciso, a nomenclatura do Estatuto da Pessoa Idosa, o destino do §4º do art. 180, a multa cominada em índice extinto e o critério para verificar um catálogo em que a maioria dos artigos compartilha moldura.',
    'O método que o arquivo protegia continua valendo, e agora vive nos campos do próprio registro. Onde a classificação depende do caso, o registro diz isso em hediondo_condicao e acao_condicao. Onde a moldura vem de outro dispositivo, diz em pena_por_remissao. Onde o dispositivo deixou de vigorar mas ainda rege fatos anteriores, diz em vigencia_ate e vigencia_nota. Nenhum deles preenche lacuna com plausibilidade — é para isso que existem.',
    'O que sobrou em aberto não é pergunta de direito, é trabalho de coleta: dispositivos com moldura própria que ainda não têm registro, apontados um a um pela revisão. Eles pertencem ao conferidor, que é quem varre a lei atrás do que falta, e é lá que serão tratados.',
  ],
  tipo: 'melhoria',
  areas: ['Documentação'],
  version: 'v2.0.0',
};

export default entrada;

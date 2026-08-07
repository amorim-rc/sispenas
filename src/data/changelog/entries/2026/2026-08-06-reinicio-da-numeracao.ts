import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-06-reinicio-da-numeracao',
  date: '2026-08-06',
  title: 'A numeração dos tipos penais recomeça em 1, e os links antigos mudam',
  summary:
    'O identificador de cada tipo penal é a URL pública dele. Com a revisão da base — nove registros retirados, noventa e seis criados —, a numeração recomeçou de 1 a 1505. É a segunda vez que isso acontece, e a última decidida sem aviso: daqui em diante o identificador volta a ser imutável.',
  body: [
    'Quem tenha guardado um endereço da forma /pesquisa/tipos?tipo=N precisa refazê-lo: o número passou a apontar para outro crime. Os links das notas de atualização já publicadas foram remapeados para o crime de que falam, e a trilha de conferência de cada registro acompanhou o novo número.',
    'A regra que volta a valer, sem exceção, é a de sempre: identificador retirado entra em ids-aposentados.json e nunca é reatribuído. Ela existe porque o modo de falhar é silencioso — um link antigo que passa a abrir outro crime não dá erro, só mostra a resposta errada.',
    'O reinício é o que torna esta versão MAIOR. Não é o tamanho da revisão: é que o contrato das URLs quebrou, e quem consome os dados abertos precisa saber disso antes de atualizar.',
  ],
  tipo: 'estrutural',
  areas: ['Tipos penais', 'Interface', 'Documentação'],
  version: 'v2.0.0',
};

export default entrada;

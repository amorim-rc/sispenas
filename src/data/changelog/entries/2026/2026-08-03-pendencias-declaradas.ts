import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-03-pendencias-declaradas',
  date: '2026-08-03',
  title: 'O que foi examinado e deixado em aberto de propósito agora tem registro',
  summary:
    'Uma revisão jurídica classificou cada resposta em três graus, e o terceiro era não publicar. O que não vira dado costuma sumir. Agora há um arquivo para isso, e a conferência semanal o repete.',
  body: [
    'A revisão de agosto de 2026 respondeu cerca de cento e cinquenta perguntas acumuladas, e classificou cada resposta em três graus de confiança: aplicável, aplicável com a divergência anotada, e questão aberta sem resposta segura. As do terceiro grupo não podiam virar dado publicado.',
    'O problema é que uma pergunta examinada e deixada em aberto não deixa rastro. Sem registro, a próxima leitura recomeça do zero, ou publica um palpite. É a informação mais cara do trabalho, e a mais fácil de perder.',
    'O arquivo de pendências guarda, para cada uma, a pergunta em uma frase, o que precisa ser visto para respondê-la, e o que fica errado ou incompleto enquanto ela existir. Onze pendências abriram o arquivo, entre elas a vigência da lei de proteção aos cetáceos frente à lei ambiental, a revogação tácita da instalação clandestina de rádio, a redação nova do art. 112 da Lei de Execução Penal e os dispositivos que substituem a moldura em vez de majorar a pena.',
    'A conferência semanal repete todas elas no relatório, como já fazia com as pendências da tabela de crimes hediondos. Uma pergunta que ninguém repete é uma pergunta que se perde, e o silêncio de uma rodada semanal passa facilmente por está tudo certo.',
  ],
  tipo: 'melhoria',
  areas: ['Documentação'],
  version: 'v1.8.0',
};

export default entrada;

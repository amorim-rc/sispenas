import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-03-pendencias-declaradas',
  date: '2026-08-03',
  title: 'As perguntas que ficaram sem resposta agora são um documento, não um arquivo de dados',
  summary:
    'Uma revisão jurídica classificou cada resposta em três graus, e o terceiro era não publicar. O que não vira dado costuma sumir. Agora há um documento para isso, escrito para ser respondido por quem não conhece o sistema.',
  body: [
    'A revisão de agosto de 2026 respondeu cerca de cento e cinquenta perguntas acumuladas, e classificou cada resposta em três graus de confiança: aplicável, aplicável com a divergência anotada, e questão aberta sem resposta segura. As do terceiro grupo não podiam virar dado publicado.',
    'O problema é que uma pergunta examinada e deixada em aberto não deixa rastro. Sem registro, a próxima leitura recomeça do zero, ou publica um palpite. É a informação mais cara do trabalho, e a mais fácil de perder.',
    'As onze perguntas que sobraram estão em REVISAO-PENDENTE.md, na raiz do repositório. Cada uma traz o contexto, o texto legal transcrito do compilado oficial, o que o catálogo publica hoje e o que se quer decidir — o documento é autossuficiente, e quem responde não precisa abrir nenhum arquivo, sistema ou base de dados.',
    'Isso é uma escolha, não uma comodidade. Quem tem condição de responder se o art. 29 da Lei de Crimes Ambientais derrogou a lei de proteção aos cetáceos, ou se o roubo com arma de uso restrito é qualificadora ou causa de aumento, é jurista — e uma pergunta que exige leitura de código para ser entendida é uma pergunta que não vai ser respondida.',
    'Entre elas: qual redação do art. 112 da Lei de Execução Penal vale, depois de ele ser reescrito duas vezes em 2026; se o crime de rádio clandestina do Código Penal sobreviveu à Lei Geral de Telecomunicações; se a equiparação constitucional do tráfico alcança o tipo militar; como representar o dispositivo que troca a moldura da pena em vez de aumentá-la; e treze registros cujo nome se parece mais com outro artigo do mesmo diploma que com o próprio.',
    'A conferência semanal repete os títulos de todas elas no relatório, como já fazia com as pendências da tabela de crimes hediondos. Uma pergunta que ninguém repete é uma pergunta que se perde, e o silêncio de uma rodada semanal passa facilmente por está tudo certo.',
  ],
  tipo: 'melhoria',
  areas: ['Documentação'],
  version: 'v1.8.0',
};

export default entrada;

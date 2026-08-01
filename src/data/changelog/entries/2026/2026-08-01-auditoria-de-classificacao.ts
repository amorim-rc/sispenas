import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-01-auditoria-de-classificacao',
  date: '2026-08-01',
  title: 'A conferência semanal passa a olhar também hediondez e ação penal',
  summary:
    'Até agora a máquina conferia a pena. Quatro campos que também decidem benefício — hediondez, ação penal, causas de aumento e o próprio nome do tipo — ficavam sem vigilância. Passam a ser auditados toda semana, cada um até onde a lei permite decidir sem juízo humano.',
  body: [
    'A hediondez não é opinião: está no artigo primeiro da Lei 8.072 de 1990, que é uma lista fechada. O texto oficial, porém, empilha todas as redações já dadas a cada inciso — o primeiro deles aparece sete vezes, de 1994 a 2025 —, e ler essa pilha por automação escolheria a versão errada em silêncio. Por isso o rol foi transcrito uma vez, à mão, para uma tabela; a máquina compara o catálogo com ela e, além disso, vigia o texto da lei: se o rol mudar, o alerta vem antes de qualquer outro resultado.',
    'A ação penal segue a regra do artigo 100 do Código Penal — é pública incondicionada, salvo quando o próprio diploma diz o contrário, em fórmulas reconhecíveis como "somente se procede mediante representação". A auditoria lê essas fórmulas no artigo do tipo. O que estiver em artigo de encerramento de capítulo, ou em outro diploma, continua fora do alcance, e isso está declarado no relatório.',
    'Nos dois campos, onde a lei condiciona a classificação a uma circunstância do caso — o homicídio praticado em atividade de grupo de extermínio, a organização criminosa direcionada a crime hediondo —, nada é proposto: a lei não decide pelo tipo, e quem decide é quem julga.',
    'Os outros dois campos rendem apenas listas para leitura. As causas de aumento presentes na lei e ausentes do catálogo de modificadores são apontadas, mas não modeladas: definir sobre quais tipos um aumento incide não se lê do dispositivo isolado. E o nome de cada tipo é comparado com o texto do artigo, para achar registro que descreve outro crime — foi assim que se descobriu que o artigo 338 do Código Penal estava publicado com o nome da sonegação previdenciária, que é o artigo 337-A.',
    'O que depende de julgamento não vira mais linha perdida num relatório: vira proposta de alteração, com o fundamento ao lado, para ser aceita ou recusada uma a uma.',
  ],
  tipo: 'novidade',
  areas: ['Tipos penais', 'Benefícios'],
  version: 'v1.6.0',
  links: [
    {
      label: 'Como os dados são coletados e revisados',
      href: 'https://amorim-rc.github.io/sispenas/docs/dados-abertos',
    },
  ],
};

export default entrada;

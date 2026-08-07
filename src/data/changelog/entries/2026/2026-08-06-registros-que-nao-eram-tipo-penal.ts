import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-06-registros-que-nao-eram-tipo-penal',
  date: '2026-08-06',
  title: 'Sete registros publicavam pena de um dispositivo que não cria crime',
  summary:
    'O catálogo contém apenas tipos penais. Sete registros não eram: dois eram regra de punibilidade, dois eram causa de aumento, um era agravante sem quantum e dois eram cópia de outro registro do mesmo dispositivo. Todos publicavam uma moldura, e uma moldura publicada entra em todo cálculo de benefício.',
  body: [
    'O §4º do art. 180 do Código Penal diz que a receptação é punível ainda que desconhecido ou isento de pena o autor do crime de que proveio a coisa. Não descreve conduta e não comina pena. O registro publicava reclusão de três a oito anos — que é a moldura do §1º, e o §1º já tinha registro próprio — sob o nome "receptação de veículo automotor", figura que o art. 180 não tem. O §2º do art. 138, que diz ser punível a calúnia contra os mortos, era o mesmo caso.',
    'Os arts. 258 e 263 do Código Penal são causas de aumento sobre os crimes de perigo comum e de perigo no transporte: aumentam de metade se resulta lesão grave, dobram se resulta morte. Já estavam no catálogo de modificadores, e o registro de tipo era o que sobrava. Ao migrá-los, corrigiu-se também o alcance: o art. 285 estende o regime do art. 258 aos crimes contra a saúde pública, salvo o art. 267, e isso não estava registrado.',
    'O §3º do art. 2º da Lei 12.850/13 agrava a pena de quem exerce o comando da organização criminosa, sem dizer quanto: é agravante da segunda fase, resolvida pelo art. 59 do Código Penal, e não tem moldura própria para publicar.',
    'Dois registros do art. 127 do Código Penal eram duplicata um do outro — o aborto qualificado pelo resultado aparecia duas vezes, sob rótulos diferentes do mesmo dispositivo. Sobrou um de cada hipótese, com a moldura conferida: a lesão grave sobre a base do art. 125 e a do art. 126 passaram a ter registros separados, porque são bases diferentes.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais', 'Dosimetria', 'Benefícios'],
  version: 'v2.0.0',
};

export default entrada;

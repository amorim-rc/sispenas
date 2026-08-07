import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-06-molduras-conferidas-uma-a-uma',
  date: '2026-08-06',
  title: 'As molduras que a conferência automática não alcançava foram lidas à mão',
  summary:
    'O conferidor semanal compara a pena publicada com a pena que a lei comina — mas só consegue fazê-lo quando a moldura está escrita no artigo. Sobravam 259 registros cuja pena é derivada de outro dispositivo, e por isso nunca passavam pela conferência. Todos foram lidos contra o texto compilado, um a um. Sessenta e sete estavam errados.',
  body: [
    'O caso maior é o das causas de aumento e diminuição que alcançam mais de uma moldura-base. O §3º do art. 122 do Código Penal duplica a pena do caput e também a dos §§ 1º e 2º: são três molduras num dispositivo só. O catálogo publicava uma delas, ou um intervalo que juntava as três e não correspondia a nenhuma. O mesmo acontecia nos §§ 4º e 10 e 12 do art. 129, no §3º dos arts. 133 e 136, no §4º do art. 159 e no parágrafo único do art. 299.',
    'Um intervalo que junta molduras diferentes não é conservador: é errado nas duas pontas. O §10 do art. 129 estava publicado como 16 a 192 meses, que era o menor mínimo de uma das bases com o maior máximo de outra — número que a lei não comina em hipótese nenhuma. Agora cada base tem seu registro, com a conta feita a partir dela.',
    'Sete registros da Lei 2.889/56 e da Lei 1.579/52 publicavam moldura de outro artigo. O art. 4º, I da lei das comissões parlamentares de inquérito manda aplicar a pena do art. 329 do Código Penal, que é detenção de dois meses a dois anos; o catálogo publicava reclusão de um a cinco anos. O inciso II remete ao art. 342, e a moldura publicada era a redação anterior à Lei 12.850/2013. No genocídio, quatro das cinco alíneas do art. 1º traziam faixas que não correspondiam a nenhum dos artigos remetidos.',
    'Dezesseis observações que contradiziam a moldura corrigida foram reescritas. O texto ao lado do registro dizia "1 a 3 anos" onde a pena publicada passou a ser de um ano e quatro meses a cinco anos e quatro meses, e num caso descrevia um aumento — de um terço na faixa de pedestres — que o artigo simplesmente não tem.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais', 'Benefícios'],
  version: 'v2.0.0',
  links: [
    {
      label: 'Ver o falso testemunho perante CPI',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=548',
    },
  ],
};

export default entrada;

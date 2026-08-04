import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-04-crimes-de-transito-nunca-conferidos',
  date: '2026-08-04',
  title: 'A conferência semanal nunca tinha lido a pena de um crime de trânsito sequer',
  summary:
    'O Código de Trânsito escreve "Penas", no plural, porque cada um dos seus crimes comina prisão e mais a suspensão da habilitação. A conferência procurava a palavra no singular. Doze dispositivos, entre eles homicídio culposo na direção e embriaguez ao volante, atravessaram todas as rodadas sem uma única comparação com a lei.',
  body: [
    'A ferramenta confronta o catálogo com o texto oficial das leis toda semana e publica quanto do catálogo foi de fato conferido. O número era honesto no que afirmava, mas escondia isto: um dispositivo cuja pena não é lida não aparece como divergente. Aparece como nada.',
    'A causa era um único caractere. A conferência reconhecia a linha de pena pela palavra "Pena" seguida de fim de palavra, e "Penas" não passa nesse teste. Todos os doze crimes do Código de Trânsito são escritos no plural, porque o preceito comina mais de uma sanção ao mesmo tempo: detenção e suspensão ou proibição de obter a habilitação.',
    'Lido o Código de Trânsito pela primeira vez, uma divergência real apareceu. O art. 310 — entregar a direção a pessoa não habilitada ou sem condições de dirigir — comina detenção de seis meses a um ano, ou multa. O catálogo publicava seis meses a três anos, com multa cumulativa e suspensão da habilitação. Nada disso está no artigo: três vezes o máximo, e uma multa alternativa transformada em cumulativa. Corrigido contra o texto oficial.',
    'Os outros onze crimes de trânsito conferem com a lei.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais', 'Benefícios'],
  version: 'v1.9.3',
};

export default entrada;

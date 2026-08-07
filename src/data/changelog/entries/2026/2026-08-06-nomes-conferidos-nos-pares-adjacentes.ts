import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-08-06-nomes-conferidos-nos-pares-adjacentes',
  date: '2026-08-06',
  title: 'Os 425 registros de maior risco de troca de nome foram relidos contra a lei',
  summary:
    'Quando dois artigos vizinhos cominam a mesma pena, trocar os nomes não produz divergência nenhuma para a conferência de molduras: a pena confere dos dois lados. Esse ponto cego já produziu erro três vezes. Os 425 registros que formam pares adjacentes de mesma moldura foram relidos contra o texto do próprio dispositivo.',
  body: [
    'A varredura mediu antes de agir. Pares de artigos com pena idêntica no mesmo diploma são 179 grupos e envolvem 70% do catálogo — molduras repetidas são a norma num código penal, não a exceção, e como filtro de risco isso não filtra nada. Restringindo a artigos adjacentes, com número consecutivo ou o mesmo número com sufixo de letra, sobraram os pares que valiam leitura humana.',
    'Os seis incisos do §2º do art. 171 do Código Penal estavam deslocados em bloco: o registro do inciso II descrevia a defraudação de penhor, que é o inciso III; o do inciso III descrevia a fraude na entrega de coisa, que é o IV; o do inciso IV descrevia a fraude no pagamento por cheque, que é o VI. Cada nome estava um degrau à frente do seu artigo, e como todos compartilham a moldura do caput, nada acusava.',
    'O mesmo deslocamento apareceu nos incisos do §1º do art. 16 do Estatuto do Desarmamento e nos do §1º do art. 29 da Lei de Crimes Ambientais, onde os três registros descreviam as hipóteses de aumento do §4º. E no art. 312 do Código Penal, um registro apontado ao §3º publicava o peculato-furto, que é o §1º e já tinha registro próprio — era duplicata pelo nome.',
    'A maior parte das correções, porém, não é de troca: é de precisão. Nomes montados por abreviação ("Induzimento a suicídio") passaram a dizer a conduta que o dispositivo descreve ("Induzimento, instigação ou auxílio a suicídio ou a automutilação"), e os incisos que só se distinguem pelo nome — como os do §2º do art. 121-A, que compartilham texto de cabeça e moldura — passaram a trazer a circunstância inteira. É o grupo de risco máximo de troca, e o nome é a única coisa que os separa.',
  ],
  tipo: 'correcao',
  areas: ['Tipos penais', 'Interface'],
  version: 'v2.0.0',
  links: [
    {
      label: 'Ver o estelionato do art. 171, §2º, II',
      href: 'https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=590',
    },
  ],
};

export default entrada;

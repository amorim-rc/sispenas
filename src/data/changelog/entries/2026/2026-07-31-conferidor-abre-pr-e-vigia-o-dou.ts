import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-31-conferidor-abre-pr-e-vigia-o-dou',
  date: '2026-07-31',
  title: 'A conferência semanal passa a propor a correção e a vigiar o Diário Oficial',
  summary:
    'O conferidor deixa de só relatar: quando a divergência é inequívoca, ele mesmo abre a proposta de correção, com a evidência de cada mudança. E ganha um segundo olho, sobre o Diário Oficial, para achar a lei penal nova que nenhuma releitura dos diplomas conhecidos revelaria.',
  body: [
    'Toda segunda-feira o sistema baixa os textos compilados dos 62 diplomas do catálogo e compara pena a pena. O que exige juízo jurídico continua indo para uma lista de triagem humana. O que é leitura de texto — a moldura ou a espécie de pena de um registro que já existe divergir do que a lei comina — passa a virar uma proposta pronta, de um diploma por vez, em que cada mudança traz ao lado o trecho da lei que a motivou.',
    'Criar registro novo continua sendo decisão de gente, e por um motivo concreto: a primeira leva automática de criação, publicada ontem, trouxe 29 registros que não eram tipos penais vigentes. Decidir se um dispositivo é crime autônomo, causa de aumento ou nada disso não é leitura de texto.',
    'O segundo olho é o Diário Oficial. A conferência relê os diplomas que já conhece, e por isso é cega para uma lei penal inteiramente nova, que ainda não está em lugar nenhum. Uma vez por semana, o sistema percorre os atos normativos da Seção 1 — leis, medidas provisórias e afins, algo em torno de cinco por semana — e separa os que citam um diploma monitorado ou trazem vocabulário penal. É uma lista para ler, não uma decisão: aparecer nela apenas significa que vale a pena abrir o texto.',
    'O processo inteiro é determinístico, sem inteligência artificial e sem inferência. Onde não há leitura segura, o achado vira pergunta na triagem da semana em vez de virar dado publicado.',
  ],
  tipo: 'novidade',
  areas: ['Documentação', 'Tipos penais'],
  version: 'v1.4.0',
  links: [
    {
      label: 'Ver o Roadmap',
      href: 'https://amorim-rc.github.io/sispenas/docs/roadmap',
    },
  ],
};

export default entrada;

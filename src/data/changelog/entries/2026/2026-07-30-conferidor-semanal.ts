import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  id: '2026-07-30-conferidor-semanal',
  date: '2026-07-30',
  title: 'O catálogo passa a ser conferido automaticamente toda semana',
  summary:
    'Entra em operação o conferidor: toda segunda-feira o sistema baixa os textos compilados dos diplomas no Planalto, compara com o catálogo e relata as divergências. O roadmap foi reorganizado em torno dessa mudança.',
  body: [
    'Até agora a defasagem do catálogo só aparecia quando alguém reabria um artigo por outro motivo. O conferidor inverte isso: a cada semana ele percorre os 62 diplomas, estrutura cada dispositivo do texto oficial, lê as molduras penais e confronta com o que está publicado — apontando penas divergentes, dispositivos revogados e crimes ausentes.',
    'É um processo determinístico, sem inteligência artificial e sem inferência: onde não há certeza, há relatório para decisão humana. Nenhum dado é alterado automaticamente, porque boa parte dos achados exige julgamento jurídico — um dispositivo novo pode ser um crime autônomo, uma causa de aumento ou nada disso. A acuidade continua sendo decidida por gente.',
    'O roadmap foi reescrito em função disso: a v2.0.0 passa a ser o catálogo conferido automaticamente, seguida do catálogo de benefícios em dados, do acervo histórico e das melhorias de usabilidade. A v3.0.0 reúne processo penal, jurisprudência e a plataforma de pesquisa.',
  ],
  tipo: 'melhoria',
  areas: ['Documentação'],
  version: 'v1.2.15',
  links: [
    {
      label: 'Ver o Roadmap',
      href: 'https://amorim-rc.github.io/sispenas/docs/roadmap',
    },
  ],
};

export default entrada;

import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  "id": "2026-07-27-notas-de-atualizacoes-em-feed",
  "date": "2026-07-27",
  "title": "Notas de atualizações reformuladas em feed",
  "summary": "A página de notas deixa de ser uma lista de posts por versão e passa a ser um feed de mudanças: cada alteração é uma entrada datada, resumida em um parágrafo, com tags de tipo e área e abertura para os detalhes.",
  "body": [
    "Os filtros ficam num menu vertical — Tipo, Área e Versão —, com multisseleção. Quando a tela aperta, o menu recolhe num botão de Filtros, o que já adapta a navegação para o celular.",
    "Cada entrada aponta, na abertura, para o local exato onde a mudança aparece no site."
  ],
  "tipo": "novidade",
  "areas": [
    "Interface",
    "Documentação"
  ],
  "version": "v1.2.1",
  "links": [
    {
      "label": "Ver o feed",
      "href": "https://amorim-rc.github.io/sispenas/release-notes"
    }
  ]
};

export default entrada;

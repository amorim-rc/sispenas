import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  "id": "2026-07-15-busca-por-beneficio",
  "date": "2026-07-15",
  "title": "Busca por benefício e catálogo declarativo",
  "summary": "Esta versão inverte o percurso de pesquisa. Até aqui só era possível partir de um tipo penal; agora se pode partir de um benefício e ver a que tipos ele alcança.",
  "body": [
    "O catálogo passou a ser declarativo, o que tornou possível calcular o alcance de cada benefício sobre todo o acervo de tipos."
  ],
  "tipo": "novidade",
  "areas": [
    "Benefícios"
  ],
  "version": "v1.1.0",
  "links": [
    {
      "label": "Ver a busca por benefício",
      "href": "https://amorim-rc.github.io/sispenas/pesquisa/beneficios"
    }
  ]
};

export default entrada;

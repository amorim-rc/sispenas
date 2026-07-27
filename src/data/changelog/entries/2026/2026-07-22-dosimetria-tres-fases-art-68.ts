import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  "id": "2026-07-22-dosimetria-tres-fases-art-68",
  "date": "2026-07-22",
  "title": "Dosimetria pelas três fases do art. 68",
  "summary": "O sistema deixa de partir da pena cominada e passa a percorrer as três fases da dosimetria — pena-base, intermediária e definitiva —, com a pena apurada alimentando os benefícios. Cada fase incide sobre uma base diferente e respeita os seus próprios limites.",
  "body": [
    "A separação por fase não é organização visual: cada fase incide sobre uma base diferente e obedece a limites próprios — e é aí que uma implementação ingênua erraria.",
    "A 1ª fase move 1/8 do intervalo da moldura por circunstância judicial e fica presa à moldura. A 2ª move 1/6 da pena-base e também fica presa à moldura, com o piso na Súmula 231 do STJ. A 3ª incide sobre a pena intermediária, com a fração própria de cada causa, e é a única que pode romper a moldura.",
    "É essa assimetria que permite a tentativa levar a pena abaixo do mínimo cominado — o que a 2ª fase jamais faria."
  ],
  "tipo": "novidade",
  "areas": [
    "Dosimetria"
  ],
  "version": "v1.2.0",
  "links": [
    {
      "label": "Ver a dosimetria no homicídio simples",
      "href": "https://amorim-rc.github.io/sispenas/pesquisa/tipos?tipo=1"
    }
  ]
};

export default entrada;

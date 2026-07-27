import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  "id": "2026-07-27-nota-da-release-montada-das-entradas",
  "date": "2026-07-27",
  "title": "A nota da Release no GitHub é montada a partir das entradas",
  "summary": "A nota grande de cada versão deixa de ser escrita à mão: o workflow de release concatena as entradas do changelog daquela versão. Um dado, dois destinos — o feed no site e o corpo da Release.",
  "body": [
    "Fonte única: as entradas. A Release no GitHub e o feed no site passam a ler a mesma coisa, e não podem mais divergir."
  ],
  "tipo": "melhoria",
  "areas": [
    "Documentação"
  ],
  "version": "v1.2.1"
};

export default entrada;

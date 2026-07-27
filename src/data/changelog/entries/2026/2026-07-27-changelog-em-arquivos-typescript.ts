import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  "id": "2026-07-27-changelog-em-arquivos-typescript",
  "date": "2026-07-27",
  "title": "Cada entrada do changelog é um arquivo próprio",
  "summary": "As notas passam a viver em arquivos TypeScript, um por entrada, agregados automaticamente. Adicionar uma nota é criar um arquivo; não há mais lista central a manter em sincronia.",
  "body": [
    "O formato foi desenhado para que um backend futuro produza exatamente o mesmo JSON sem tocar no frontend.",
    "O fluxo de criação está documentado em create-changelog-entry, com regras para que uma IA produza esses arquivos corretamente."
  ],
  "tipo": "melhoria",
  "areas": [
    "Documentação"
  ],
  "version": "v1.2.1"
};

export default entrada;

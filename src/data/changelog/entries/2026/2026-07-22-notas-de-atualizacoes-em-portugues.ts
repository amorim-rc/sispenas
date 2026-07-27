import type {ChangelogEntry} from '../../types';

const entrada: ChangelogEntry = {
  "id": "2026-07-22-notas-de-atualizacoes-em-portugues",
  "date": "2026-07-22",
  "title": "“Notas de atualizações” no lugar de “Release notes”",
  "summary": "A aba do changelog passa a ter nome em português. A rota /release-notes foi mantida de propósito: mudá-la quebraria links já publicados.",
  "body": [
    "Pela tabela de versionamento, mudar a rota seria alteração estrutural (X.0.0), porque quebra URLs públicas — por isso só o rótulo mudou."
  ],
  "tipo": "melhoria",
  "areas": [
    "Interface"
  ],
  "version": "v1.2.0"
};

export default entrada;

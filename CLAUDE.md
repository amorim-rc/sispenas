# Instruções para agentes de IA — SISPENAS

Ferramenta aberta de pesquisa de tipos penais e benefícios. **Acuidade jurídica é o valor
central**: um dado errado publicado é pior que um dado ausente. Nada entra no catálogo sem
conferência contra o **texto compilado** oficial do `planalto.gov.br`.

## Fluxo de release — OBRIGATÓRIO em toda atuação

O projeto publica **duas coisas** a cada versão: a Release no GitHub (para colaboradores) e
a release note no site (para quem acompanha). Ambas saem do **mesmo arquivo**. Por isso:

1. **Toda mudança substantiva atualiza a release note da versão corrente** em
   `release-notes/`. Enquanto se trabalha rumo à versão `X.Y.Z`, mantenha (criando se
   preciso) `release-notes/AAAA-MM-DD-vX.Y.Z.md`, acrescentando ali o que a mudança fez.
   Correções de dado, novos tipos/benefícios, fixes e ajustes de interface contam;
   mudança interna trivial (comentário, refactor sem efeito) não precisa.

2. **Versione segundo `docs/roadmap.md`** (semver com significado explícito): correção de
   dado ou bug → `1.1.Z`; funcionalidade nova compatível → `1.Y.0`; quebra de contrato dos
   dados abertos ou das URLs → `X.0.0`.

3. **Para publicar, o PR que FECHA a versão sobe `version` em `package.json` (e em
   `CITATION.cff`).** Ao mergear na `main`, o workflow `.github/workflows/release.yml`
   detecta a versão nova, cria a tag `vX.Y.Z` e publica a Release com o texto da release
   note. **Não faça `git push origin vX.Y.Z` manual** — é automático.

Resumo: *escreveu a release note + subiu a versão + mergeou → release publicada, no GitHub
e no site.*

## Convenções do catálogo

Estão em `CONTRIBUTING.md` (C1–C8) e são **impostas pela CI**. As que quebram em silêncio se
ignoradas:

- `data/crimes.json` é a **fonte**; `static/data/crimes.json` é **derivado** por
  `scripts/transform_data.py` — teste sempre contra o derivado.
- `id` é **append-only**: é a URL pública (`?tipo=N`). Nunca reatribua nem renumere.
- `resultado_morte` deriva do **nome** do tipo, nunca do `obs`.
- Editar `.md` com Python/`sed` no Windows introduz **CRLF** (quebra os admonitions
  `:::note[...]`); use `write_bytes` ou confira o EOL.
- Admonitions do Docusaurus v3: `:::note[Título]`, não `:::note Título`.

## Verificação antes de concluir

```
python scripts/transform_data.py --estrito --max-contradicoes=0
npm run typecheck
npm run verificar
npm run build
```

A CI trava em `--max-contradicoes=0` e exige o derivado sincronizado com a fonte. Extraia
PDFs de leis com `pdftotext -layout -enc UTF-8` (o poppler não renderiza página aqui).

Trabalhe em branch própria, commits pequenos e descritivos; **não faça push nem abra PR sem
o usuário pedir**.

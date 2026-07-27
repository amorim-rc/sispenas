// Agrega todas as entradas de entries/**/*.ts, ordenadas da mais recente para a
// mais antiga. NÃO há lista central: adicionar uma entrada = criar um arquivo.
//
// require.context é resolvido pelo bundler (Rspack/Webpack) em tempo de build.
// O gerador de JSON para o CI (scripts/gerar-changelog-json.mjs) percorre os
// mesmos arquivos por glob — os dois caminhos produzem o mesmo array.

import type {ChangelogEntry} from './types';

type Contexto = {
  keys(): string[];
  (id: string): {default: ChangelogEntry};
};

const ctx = (
  require as unknown as {context(d: string, r: boolean, re: RegExp): Contexto}
).context('./entries', true, /\.ts$/);

/** Mais recentes primeiro; empate de data resolve pelo id (desc), estável. */
export function ordenar(entradas: ChangelogEntry[]): ChangelogEntry[] {
  return [...entradas].sort((a, b) => {
    if (a.date !== b.date) return a.date < b.date ? 1 : -1;
    return a.id < b.id ? 1 : -1;
  });
}

const entries: ChangelogEntry[] = ordenar(
  ctx.keys().map((k) => ctx(k).default),
);

export default entries;

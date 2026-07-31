// Impede que o feed anuncie versão que ainda não existe.
//
// Aconteceu: três entradas foram escritas com v1.2.16, v1.2.17 e v1.2.18
// enquanto o `package.json` seguia em 1.2.15, porque o bump era feito por
// substituição de texto e falhava em silêncio quando a versão de origem não
// batia. O feed prometia releases que nunca saíram.
//
// Duas regras, ambas verificáveis sem rede e sem depender de tags — o checkout
// da CI nem sempre as traz, e a primeira versão desta checagem quebrou por isso:
//
//   1. nenhuma entrada pode citar versão MAIOR que a do `package.json` — é o
//      sintoma exato do bump que não aconteceu;
//   2. a versão atual precisa ter ao menos uma entrada, senão a release sai com
//      corpo vazio.
import {readFileSync} from 'node:fs';

import {lerEntradas} from './_ler-changelog.mjs';

/** Compara "v1.2.10" com "v1.3.0" por número, não por texto. */
function comparar(a, b) {
  const pa = a.replace(/^v/, '').split('.').map(Number);
  const pb = b.replace(/^v/, '').split('.').map(Number);
  for (let i = 0; i < 3; i++) {
    if ((pa[i] ?? 0) !== (pb[i] ?? 0)) return (pa[i] ?? 0) < (pb[i] ?? 0) ? -1 : 1;
  }
  return 0;
}

const atual = `v${JSON.parse(readFileSync('package.json', 'utf8')).version}`;
const entradas = await lerEntradas();

const futuras = entradas
  .filter((e) => e.version && comparar(e.version, atual) > 0)
  .map((e) => `${e.id} -> ${e.version}`);

if (futuras.length) {
  console.error(
    `✗ ${futuras.length} entrada(s) anunciam versão posterior à do projeto (${atual}):`);
  for (const f of futuras) console.error(`  ${f}`);
  console.error('\nProvável causa: o bump de versão não foi aplicado.');
  process.exit(1);
}

if (!entradas.some((e) => e.version === atual)) {
  console.error(`✗ nenhuma entrada carrega a versão atual (${atual}) — a release ` +
    'sairia com corpo vazio.');
  process.exit(1);
}

console.log(`✓ changelog coerente com ${atual} (${entradas.length} entradas)`);

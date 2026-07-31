// Impede que entrada do changelog aponte para versão que não existe.
//
// Aconteceu: três entradas foram escritas com v1.2.16, v1.2.17 e v1.2.18
// enquanto o `package.json` seguia em 1.2.15, porque o bump era feito por
// substituição de texto e falhava em silêncio quando a versão de origem não
// batia. O feed anunciava versões que nunca foram publicadas.
//
// Regra: toda entrada precisa citar a versão ATUAL do package.json ou uma que
// já tenha sido lançada (tag no repositório).
import {execSync} from 'node:child_process';
import {readFileSync} from 'node:fs';

import {lerEntradas} from './_ler-changelog.mjs';

const atual = `v${JSON.parse(readFileSync('package.json', 'utf8')).version}`;
const tags = new Set(
  execSync('git tag --list "v*"', {encoding: 'utf8'}).split('\n').map((t) => t.trim()),
);

const orfas = (await lerEntradas())
  .filter((e) => e.version && e.version !== atual && !tags.has(e.version))
  .map((e) => `${e.id} -> ${e.version}`);

if (orfas.length) {
  console.error(`✗ ${orfas.length} entrada(s) apontam para versão inexistente ` +
    `(atual: ${atual}):`);
  for (const o of orfas) console.error(`  ${o}`);
  console.error('\nOu a versão do package.json não subiu, ou a entrada cita a versão errada.');
  process.exit(1);
}
console.log(`✓ changelog coerente com ${atual}`);

// Emite static/data/changelog.json — o mesmo array de ChangelogEntry que o
// frontend agrega, num único JSON. Serve à paridade com um backend futuro e a
// consumidores externos. Rodar: node scripts/gerar-changelog-json.mjs

import {mkdirSync, writeFileSync} from 'node:fs';
import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {lerEntradas} from './_ler-changelog.mjs';

const AQUI = dirname(fileURLToPath(import.meta.url));
const SAIDA = join(AQUI, '..', 'static', 'data', 'changelog.json');

const entradas = await lerEntradas();
mkdirSync(dirname(SAIDA), {recursive: true});
writeFileSync(SAIDA, JSON.stringify(entradas, null, 2) + '\n', 'utf-8');
console.log(`${entradas.length} entradas -> static/data/changelog.json`);

/**
 * Verificação do motor de benefícios contra o catálogo real de tipos penais.
 *
 * Não é um substituto da revisão jurídica: checa invariantes estruturais do
 * motor e um conjunto de casos-âncora cuja resposta legal é pacífica.
 *
 * Uso: npm run verificar
 */

import * as fs from 'fs';
import * as path from 'path';
import type {Crime} from '../src/lib/types';
import {CATALOGO, avaliarBeneficio, valoresPadrao} from '../src/lib/beneficios';
import {avaliarCatalogo, cenarioReversoPadrao, contar} from '../src/lib/beneficios/reverso';
import {cenarioFromCrime} from '../src/lib/cenario';

// Lê o MESMO arquivo servido à aplicação (static/data/crimes.json), e não a fonte
// bruta em data/crimes.json: os campos derivados (pena_min_meses, pena_privativa,
// infracao_menor_potencial…) só existem após scripts/transform_data.py.
// Executado a partir da raiz do projeto (ver script "verificar" no package.json).
const crimes: Crime[] = JSON.parse(
  fs.readFileSync(path.join(process.cwd(), 'static', 'data', 'crimes.json'), 'utf-8'),
);

let falhas = 0;
const ok = (cond: boolean, msg: string) => {
  if (!cond) {
    falhas += 1;
    console.error(`  ✗ ${msg}`);
  } else {
    console.log(`  ✓ ${msg}`);
  }
};

/** Localiza um tipo penal pelo artigo e lei (primeira ocorrência). */
function achar(lei: RegExp, artigo: RegExp, nome?: RegExp): Crime | undefined {
  return crimes.find(
    (c) => lei.test(c.lei) && artigo.test(c.artigo) && (!nome || nome.test(c.crime)),
  );
}

console.log(`\nCatálogo: ${crimes.length} tipos penais, ${CATALOGO.length} benefícios.\n`);

// ── 1. Invariantes estruturais do registro ──────────────────────────────
console.log('1. Integridade do registro de benefícios');
{
  const ids = CATALOGO.map((b) => b.id);
  ok(new Set(ids).size === ids.length, 'ids de benefício são únicos');
  ok(
    CATALOGO.every((b) => b.requisitos.length > 0),
    'todo benefício declara ao menos um requisito',
  );
  ok(
    CATALOGO.every((b) => b.fundamento.trim().length > 0),
    'todo benefício cita fundamento legal',
  );
  ok(
    CATALOGO.every((b) => new Set(b.parametros.map((p) => p.id)).size === b.parametros.length),
    'ids de parâmetro são únicos dentro de cada benefício',
  );
  ok(
    CATALOGO.every((b) =>
      b.parametros.every((p) =>
        p.tipo === 'booleano'
          ? typeof p.padrao === 'boolean'
          : typeof p.padrao === 'number' &&
            p.padrao >= (p.min ?? 0) &&
            p.padrao <= (p.max ?? Infinity),
      ),
    ),
    'todo parâmetro tem padrão do tipo correto e dentro dos limites do controle',
  );
}

// ── 2. O motor avalia todo o catálogo sem exceção ───────────────────────
console.log('\n2. Robustez do motor sobre o catálogo real');
{
  let erros = 0;
  for (const b of CATALOGO) {
    for (const c of crimes) {
      try {
        const r = avaliarBeneficio(b, cenarioFromCrime(c), valoresPadrao(b));
        if (!r.status || !r.resumo) erros += 1;
      } catch {
        erros += 1;
      }
    }
  }
  ok(erros === 0, `${CATALOGO.length} benefícios × ${crimes.length} tipos avaliados sem erro`);
}

// ── 3. Casos-âncora: respostas juridicamente pacíficas ──────────────────
console.log('\n3. Casos-âncora de direito penal');
{
  const rev = cenarioReversoPadrao();
  const status = (beneficioId: string, c: Crime) => {
    const def = CATALOGO.find((b) => b.id === beneficioId)!;
    return avaliarBeneficio(def, cenarioFromCrime(c), valoresPadrao(def)).status;
  };

  // Homicídio simples (art. 121, CP): 6 a 20 anos, violento.
  const homicidio = achar(/^CP$/i, /121/, /homic[íi]dio simples/i);
  if (homicidio) {
    ok(status('transacao', homicidio) === 'incabivel', 'homicídio simples: transação penal incabível');
    ok(status('sursis-processual', homicidio) === 'incabivel', 'homicídio simples: sursis processual incabível');
    ok(status('anpp', homicidio) === 'incabivel', 'homicídio simples: ANPP incabível');
    ok(status('substituicao', homicidio) === 'incabivel', 'homicídio simples: substituição por PRD incabível');
  } else {
    console.log('  — homicídio simples não localizado no catálogo (verificação pulada)');
  }

  // Furto simples (art. 155, CP): 1 a 4 anos, sem violência.
  const furto = achar(/^CP$/i, /155, caput/i, /furto/i);
  if (furto) {
    ok(status('anpp', furto) === 'condicional', 'furto simples: ANPP condicional (depende de confissão)');
    ok(status('sursis-processual', furto) === 'cabivel', 'furto simples: sursis processual cabível (mín. 1 ano)');
    ok(
      status('arrependimento-posterior', furto) === 'condicional',
      'furto simples: arrependimento posterior condicional (depende de reparação)',
    );
  } else {
    console.log('  — furto simples não localizado no catálogo (verificação pulada)');
  }

  // Vedações por hediondez atingem apenas hediondos.
  const hediondos = crimes.filter((c) => c.hediondo === 'Sim');
  const naoHediondos = crimes.filter((c) => c.hediondo !== 'Sim');
  ok(
    hediondos.every((c) => status('graca', c) === 'incabivel'),
    `graça incabível em todos os ${hediondos.length} tipos hediondos (art. 5º, XLIII, CF)`,
  );
  ok(
    naoHediondos.every((c) => status('graca', c) !== 'incabivel'),
    'graça não é vedada em nenhum tipo não hediondo',
  );

  // Detração e remição independem de pena: alcançam todo o catálogo.
  for (const id of ['detracao', 'remicao']) {
    const def = CATALOGO.find((b) => b.id === id)!;
    const linhas = avaliarCatalogo(def, valoresPadrao(def), crimes, rev);
    ok(contar(linhas).cabivel === crimes.length, `${def.nome}: cabível em todos os ${crimes.length} tipos`);
  }
}

// ── 4. Monotonicidade: elevar um teto não pode reduzir o alcance ────────
console.log('\n4. Monotonicidade dos patamares (busca reversa)');
{
  const rev = cenarioReversoPadrao();
  const casos: [string, string][] = [
    ['anpp', 'limiteMinMeses'],
    ['transacao', 'limiteMaxMeses'],
    ['sursis-processual', 'limiteMinMeses'],
    ['substituicao', 'limiteConcretaMeses'],
  ];
  // "Alcance" = tipos NÃO incabíveis. Contar apenas `cabivel` tornaria o teste
  // vazio para benefícios que dependem de requisito subjetivo (o ANPP, sem
  // confissão, nunca passa de `condicional`).
  const alcance = (params: ReturnType<typeof valoresPadrao>, def: (typeof CATALOGO)[number]) => {
    const c = contar(avaliarCatalogo(def, params, crimes, rev));
    return c.cabivel + c.condicional;
  };
  for (const [beneficioId, paramId] of casos) {
    const def = CATALOGO.find((b) => b.id === beneficioId)!;
    const padrao = valoresPadrao(def);
    const base = alcance(padrao, def);
    const ampliado = alcance({...padrao, [paramId]: (padrao[paramId] as number) * 2}, def);
    const reduzido = alcance({...padrao, [paramId]: 0}, def);
    ok(
      ampliado >= base && reduzido <= base && ampliado > reduzido,
      `${def.nome}: dobrar "${paramId}" amplia (${base}→${ampliado}) e zerar reduz (${base}→${reduzido})`,
    );
  }
}

// ── 5. Alcance de cada benefício sob a legislação vigente ───────────────
console.log('\n5. Alcance sob a legislação vigente (pena concreta = mínima cominada)');
{
  const rev = cenarioReversoPadrao();
  for (const def of CATALOGO) {
    const c = contar(avaliarCatalogo(def, valoresPadrao(def), crimes, rev));
    const pct = ((c.cabivel / crimes.length) * 100).toFixed(1);
    console.log(
      `  ${def.nome.padEnd(52)} cabível ${String(c.cabivel).padStart(5)} (${pct.padStart(5)}%)  condicional ${String(c.condicional).padStart(5)}  incabível ${String(c.incabivel).padStart(5)}`,
    );
  }
}

console.log(falhas === 0 ? '\n✓ Todas as verificações passaram.\n' : `\n✗ ${falhas} verificação(ões) falharam.\n`);
process.exit(falhas === 0 ? 0 : 1);

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
import type {Cenario, Crime} from '../src/lib/types';
import {CATALOGO, avaliarBeneficio, valoresPadrao} from '../src/lib/beneficios';
import {
  avaliarCatalogo,
  cenarioReversoPadrao,
  contar,
  crimesComPenaPrivativa,
} from '../src/lib/beneficios/reverso';
import {cenarioFromCrime} from '../src/lib/cenario';
import {calcularConcurso, calcularDosimetria} from '../src/lib/dosimetria';

// Lê o MESMO arquivo servido à aplicação (static/data/crimes.json), e não a fonte
// bruta em data/crimes.json: os campos derivados (pena_min_meses, pena_privativa,
// infracao_menor_potencial…) só existem após scripts/transform_data.py.
// Executado a partir da raiz do projeto (ver script "verificar" no package.json).
const todos: Crime[] = JSON.parse(
  fs.readFileSync(path.join(process.cwd(), 'static', 'data', 'crimes.json'), 'utf-8'),
);
// Estatísticas de alcance só sobre tipos penais que cominam pena privativa.
const crimes = crimesComPenaPrivativa(todos);

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

console.log(
  `\nCatálogo: ${todos.length} tipos penais (${crimes.length} com pena privativa), ` +
    `${CATALOGO.length} benefícios.\n`,
);

// ── 0. Integridade dos campos que o motor lê do catálogo ────────────────
console.log('0. Integração catálogo → motor de benefícios');
{
  const campos: (keyof Crime)[] = [
    'tem_pena_privativa',
    'resultado_morte',
    'perdao_judicial_previsto',
    'pena_min_meses',
    'pena_max_meses',
  ];
  for (const campo of campos) {
    ok(
      todos.every((c) => c[campo] !== undefined),
      `todo registro tem o campo "${String(campo)}" (rode scripts/transform_data.py se falhar)`,
    );
  }
  ok(
    crimes.every((c) => c.pena_max_meses > 0 || c.pena_min_meses > 0),
    'todo tipo com pena privativa tem pena > 0',
  );
  // O catálogo contém APENAS tipos penais: notas de referência, agravantes e
  // excludentes foram removidas na v1.1.0.
  ok(
    !todos.some((c) => /REFER[ÊE]NCIA|EXCLUDENTE/i.test(c.crime)),
    'nenhuma nota de referência ou excludente sobrou no catálogo',
  );
  // Quem não tem pena privativa declara uma sanção: ou `sancoes_nao_privativas`
  // (art. 28, Lei 11.343/06) ou multa isolada (art. 146-A, caput — bullying).
  ok(
    todos
      .filter((c) => !c.tem_pena_privativa)
      .every((c) => (c.sancoes_nao_privativas ?? []).length > 0 || c.tem_multa),
    'todo tipo sem pena privativa declara sanção (não privativa ou multa)',
  );
  // O perdão judicial não se estende por analogia: o campo é curado, não inferido.
  ok(
    todos.some((c) => c.perdao_judicial_previsto) &&
      todos.filter((c) => c.perdao_judicial_previsto).length < todos.length * 0.1,
    `perdão judicial previsto em ${todos.filter((c) => c.perdao_judicial_previsto).length} tipos (lista curada, não inferida do elemento culposo)`,
  );
  ok(
    !todos.some((c) => c.perdao_judicial_previsto && /^CPM/.test(c.lei)),
    'nenhum tipo do CPM recebeu perdão judicial por casamento indevido de "^CP"',
  );
  // Vigência: o registro que já não vige continua no catálogo, para o fato
  // anterior, mas tem de dizer desde quando e o que se aplica no lugar.
  ok(
    todos.every((c) => c.vigente !== undefined),
    'todo registro tem o campo "vigente"',
  );
  const naoVigentes = todos.filter((c) => c.vigente === false);
  ok(
    naoVigentes.every((c) => !!c.vigencia_ate && !!c.vigencia_nota),
    `${naoVigentes.length} registro(s) não vigente(s), todos com data e nota do que houve`,
  );
  ok(
    naoVigentes.every((c) => c.tem_pena_privativa || (c.sancoes_nao_privativas ?? []).length > 0 || c.tem_multa),
    'registro não vigente continua declarando sua sanção — é consultável para fato anterior',
  );
}

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

  // Perdão judicial: só onde a lei prevê expressamente (art. 107, IX, CP).
  const homCulposo = achar(/^CP$/i, /^Art\. 121, §3º/, /homic[íi]dio culposo/i);
  if (homCulposo) {
    ok(
      homCulposo.perdao_judicial_previsto === true,
      'homicídio culposo (art. 121, §3º): perdão judicial previsto (art. 121, §5º)',
    );
    ok(
      status('perdao-judicial', homCulposo) === 'condicional',
      'homicídio culposo: perdão judicial condicional',
    );
  }
  if (furto) {
    ok(
      furto.perdao_judicial_previsto === false,
      'furto simples: SEM previsão de perdão judicial (não se estende por analogia)',
    );
    ok(status('perdao-judicial', furto) === 'incabivel', 'furto simples: perdão judicial incabível');
  }

  // Tipo penal SEM PENA MÍNIMA cominada (só teto): "detenção até 3 meses".
  // Zero na mínima não é "sem pena" — o tipo é punível e os benefícios que
  // dependem da mínima lhe são os mais favoráveis possíveis.
  const semMinima = crimes.filter((c) => c.pena_max_meses > 0 && c.pena_min_meses === 0);
  ok(semMinima.length > 0, `${semMinima.length} tipos sem pena mínima cominada (só teto) no catálogo`);
  if (semMinima.length > 0) {
    ok(
      semMinima.every((c) => status('sursis-processual', c) !== 'incabivel'),
      'tipos sem pena mínima: suspensão condicional do processo nunca incabível por quantum',
    );
    ok(
      semMinima.every((c) => /^até /.test(c.pena_faixa_rotulo)),
      'tipos sem pena mínima exibem a faixa como "até X", não como "0 a X"',
    );
  }
  // A pena mínima nunca supera a máxima — inconsistência que inverteria os limiares.
  ok(
    crimes.every((c) => c.pena_min_meses <= c.pena_max_meses),
    'pena mínima <= pena máxima em todo o catálogo',
  );

  // Resultado morte vem do catálogo, não de um interruptor global.
  const latrocinio = crimes.find((c) => /latroc[íi]nio/i.test(c.crime));
  if (latrocinio) {
    ok(latrocinio.resultado_morte === true, 'latrocínio: resultado_morte marcado no catálogo');
  }
  const omissaoSocorro = achar(/^CP$/i, /^Art\. 135$/, /omiss[ãa]o de socorro/i);
  if (omissaoSocorro) {
    ok(
      omissaoSocorro.resultado_morte === false,
      'omissão de socorro (caput): resultado_morte NÃO marcado (obs cita a morte de outro parágrafo)',
    );
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

  // ── Art. 112 da LEP: os percentuais e as quatro vedações de livramento ──
  // Um caso-âncora por hipótese. Os cenários são montados à mão porque duas
  // delas dependem de circunstância do RÉU (reincidência, comando de facção),
  // que não se lê do tipo penal.
  {
    const progressaoDef = CATALOGO.find((b) => b.id === 'progressao')!;
    const livramentoDef = CATALOGO.find((b) => b.id === 'livramento')!;
    const avaliar = (def: (typeof CATALOGO)[number], c: Crime, ajustes: Partial<Cenario>) =>
      avaliarBeneficio(def, {...cenarioFromCrime(c), ...ajustes}, valoresPadrao(def));

    // Inciso V — hediondo primário, sem resultado morte: 70%, livramento aos 2/3.
    const trafico = achar(/11\.343/, /^Art\. 33, caput/);
    if (trafico) {
      const r = avaliar(progressaoDef, trafico, {});
      ok(/70%/.test(r.resumo), `tráfico (art. 33, caput): progressão a 70% — inciso V (obtido "${r.resumo}")`);
      ok(
        avaliar(livramentoDef, trafico, {}).status === 'cabivel',
        'tráfico (art. 33, caput): livramento condicional cabível — o inciso V não o veda',
      );
    }

    // Inciso VI, "a" — hediondo com resultado morte, primário: 75%, livramento VEDADO.
    const latrocinioTipo = achar(/^CP$/i, /^Art\. 157, §3º/, /latroc/i);
    if (latrocinioTipo) {
      const r = avaliar(progressaoDef, latrocinioTipo, {});
      ok(/75%/.test(r.resumo), `latrocínio: progressão a 75% — inciso VI, "a" (obtido "${r.resumo}")`);
      ok(
        avaliar(livramentoDef, latrocinioTipo, {}).status === 'incabivel',
        'latrocínio, primário: livramento condicional VEDADO (art. 112, VI, "a", LEP)',
      );
    }

    // Inciso VI, "b" — comando de facção ultraviolenta: 75%, livramento VEDADO.
    // A hipótese não depende do resultado morte: sem ela, este mesmo réu cairia
    // no inciso V (70%) e teria livramento aos 2/3.
    if (trafico) {
      const r = avaliar(progressaoDef, trafico, {comandoOrgcrimUltraviolenta: true});
      ok(
        /75%/.test(r.resumo),
        `tráfico + comando de facção ultraviolenta: progressão a 75% — inciso VI, "b" (obtido "${r.resumo}")`,
      );
      ok(
        avaliar(livramentoDef, trafico, {comandoOrgcrimUltraviolenta: true}).status === 'incabivel',
        'comando de facção ultraviolenta: livramento condicional VEDADO (art. 112, VI, "b", LEP)',
      );
    }

    // Inciso VI, "d" — feminicídio primário: 75%, livramento VEDADO. Substitui o
    // inciso VI-A (55%, Lei 14.994/2024), revogado pela Lei 15.358/2026.
    const feminicidio = achar(/^CP$/i, /^Art\. 121-A, caput/);
    if (feminicidio) {
      ok(feminicidio.hediondo === 'Sim', 'feminicídio: hediondo no catálogo (art. 1º, I-B, Lei 8.072/90)');
      const r = avaliar(progressaoDef, feminicidio, {});
      ok(
        /75%/.test(r.resumo),
        `feminicídio, primário: progressão a 75% — inciso VI, "d" (obtido "${r.resumo}")`,
      );
      ok(
        avaliar(livramentoDef, feminicidio, {}).status === 'incabivel',
        'feminicídio, primário: livramento condicional VEDADO (art. 112, VI, "d", LEP)',
      );
    }

    // Inciso VIII — reincidente em hediondo com resultado morte: 85%, vedado.
    if (latrocinioTipo) {
      const ajuste = {primario: false, reincidenteEspecifico: true};
      const r = avaliar(progressaoDef, latrocinioTipo, ajuste);
      ok(
        /85%/.test(r.resumo),
        `latrocínio, reincidente específico: progressão a 85% — inciso VIII (obtido "${r.resumo}")`,
      );
      ok(
        avaliar(livramentoDef, latrocinioTipo, ajuste).status === 'incabivel',
        'latrocínio, reincidente específico: livramento condicional VEDADO (art. 112, VIII, LEP)',
      );
    }

    // Os dois tipos da Lei 15.358/2026: o §4º, III do art. 2º veda o livramento
    // por dispositivo próprio, e o art. 3º o herda pelo parágrafo único.
    const dominio = achar(/15\.358/, /^Art\. 2º/);
    if (dominio) {
      ok(dominio.hediondo === 'Sim', 'domínio social estruturado: hediondo (art. 1º, § único, VIII, Lei 8.072/90)');
      ok(
        dominio.pena_min_meses === 240 && dominio.pena_max_meses === 480,
        'domínio social estruturado: moldura de 20 a 40 anos',
      );
    }
  }

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

// ── 6. Dosimetria por fases (art. 68) ──────────────────────────────────
// Casos-âncora conferidos contra a planilha de referência de dosimetria.
console.log('\n6. Dosimetria por fases (art. 68, CP)');
{
  // Homicídio simples: 6 a 20 anos → 72 a 240 meses; intervalo 168.
  const homicidio = {pena_min_meses: 72, pena_max_meses: 240} as Crime;

  // 1ª fase: cada circunstância judicial desfavorável soma 1/8 do intervalo (21).
  const umaJudicial = calcularDosimetria(homicidio, [{id: 'jud-culpabilidade'}]);
  ok(umaJudicial.penaBase === 93, `1ª fase: 1 circunstância desfavorável → 72 + 21 = 93 (obtido ${umaJudicial.penaBase})`);

  const duasJudiciais = calcularDosimetria(homicidio, [
    {id: 'jud-culpabilidade'}, {id: 'jud-antecedentes'},
  ]);
  ok(duasJudiciais.penaBase === 114, `1ª fase: 2 desfavoráveis → 72 + 42 = 114 (obtido ${duasJudiciais.penaBase})`);

  // 1ª fase não ultrapassa a moldura, mesmo com as 8 desfavoráveis.
  const todasJudiciais = calcularDosimetria(homicidio, [
    'jud-culpabilidade', 'jud-antecedentes', 'jud-conduta-social', 'jud-personalidade',
    'jud-motivos', 'jud-circunstancias', 'jud-consequencias', 'jud-comportamento-vitima',
  ].map((id) => ({id})));
  ok(todasJudiciais.penaBase === 240, `1ª fase: 8 desfavoráveis não passam do máximo (obtido ${todasJudiciais.penaBase})`);

  // 2ª fase: agravante = 1/6 da pena-base (114/6 = 19).
  const comAgravante = calcularDosimetria(homicidio, [
    {id: 'jud-culpabilidade'}, {id: 'jud-antecedentes'}, {id: 'agravante-reincidencia'},
  ]);
  ok(comAgravante.penaIntermediaria === 133, `2ª fase: 114 + 1/6 = 133 (obtido ${comAgravante.penaIntermediaria})`);

  // Súmula 231: atenuante sozinha não reduz abaixo do mínimo.
  const soAtenuante = calcularDosimetria(homicidio, [{id: 'atenuante-confissao'}]);
  ok(soAtenuante.penaIntermediaria === 72 && soAtenuante.sumula231Aplicada,
    `2ª fase: atenuante no piso não reduz abaixo do mínimo — Súmula 231 (obtido ${soAtenuante.penaIntermediaria})`);

  // 3ª fase: a tentativa PODE levar abaixo do mínimo legal.
  const tentado = calcularDosimetria(homicidio, [{id: 'tentativa'}]);
  ok(tentado.penaDefinitiva < 72,
    `3ª fase: tentativa (−1/3) rompe o piso da moldura → ${tentado.penaDefinitiva} < 72`);

  // Encadeamento completo do exemplo da planilha: 114 → 133 → −1/3 = 88.7.
  const completo = calcularDosimetria(homicidio, [
    {id: 'jud-culpabilidade'}, {id: 'jud-antecedentes'},
    {id: 'agravante-reincidencia'}, {id: 'tentativa'},
  ]);
  ok(completo.penaDefinitiva === 88.7,
    `três fases encadeadas: 114 → 133 → 88.7 (obtido ${completo.penaDefinitiva})`);

  // Concurso material soma; formal exasperado é limitado pela soma (art. 70, par. único).
  const material = calcularConcurso([72, 48], 'material');
  ok(material.total === 120, `concurso material: 72 + 48 = 120 (obtido ${material.total})`);

  const formal = calcularConcurso([72, 48], 'formal', 1 / 6);
  ok(formal.total === 84, `concurso formal: maior (72) + 1/6 = 84 (obtido ${formal.total})`);

  const formalExcessivo = calcularConcurso([72, 6], 'formal', 1 / 2);
  ok(formalExcessivo.total === 78,
    `art. 70, par. único: exasperação (108) excede a soma (78) → aplica a soma (obtido ${formalExcessivo.total})`);
}

console.log(falhas === 0 ? '\n✓ Todas as verificações passaram.\n' : `\n✗ ${falhas} verificação(ões) falharam.\n`);
process.exit(falhas === 0 ? 0 : 1);

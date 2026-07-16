import React, {useEffect, useMemo, useState} from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import type {Crime} from '@site/src/lib/types';
import {
  CATEGORIA_CURTA,
  NATUREZA_LABEL,
  foiEditado,
  valoresPadrao,
  type BeneficioDef,
  type ParametroDef,
  type Parametros,
  type Status,
} from '@site/src/lib/beneficios';
import {
  BASE_AJUDA,
  BASE_LABEL,
  avaliarCatalogo,
  cenarioReversoPadrao,
  contar,
  crimesComPenaPrivativa,
  type BasePenaConcreta,
  type CenarioReverso,
} from '@site/src/lib/beneficios/reverso';
import {formatPena, formatFracao} from '@site/src/lib/format';
import styles from './styles.module.css';

const PAGE_SIZE = 40;

const STATUS_LABEL: Record<Status, string> = {
  cabivel: 'Cabível',
  condicional: 'Condicional',
  incabivel: 'Incabível',
};

function Ajuda({texto}: {texto: string}) {
  return (
    <span className={styles.ajuda} tabIndex={0} role="note" aria-label={texto} title={texto}>
      ?<span className={styles.ajudaBalao}>{texto}</span>
    </span>
  );
}

/** Valor de um parâmetro na unidade natural do seu tipo. */
function formatValor(d: ParametroDef, v: number | boolean): string {
  switch (d.tipo) {
    case 'meses':
      return formatPena(v as number);
    case 'fracao':
      return formatFracao(v as number);
    case 'inteiro':
      return String(v);
    case 'booleano':
      return (v as boolean) ? 'Sim' : 'Não';
  }
}

function ControleParametro({
  def,
  valor,
  padrao,
  onChange,
}: {
  def: ParametroDef;
  valor: number | boolean;
  padrao: number | boolean;
  onChange: (v: number | boolean) => void;
}) {
  const alterado = valor !== padrao;

  if (def.tipo === 'booleano') {
    return (
      <label className={`${styles.paramBool} ${alterado ? styles.paramAlterado : ''}`}>
        <input
          type="checkbox"
          checked={valor as boolean}
          onChange={(e) => onChange(e.target.checked)}
        />
        <span className={styles.paramRotulo}>
          {def.rotulo}
          <Ajuda texto={def.ajuda} />
        </span>
        {def.fundamento && <span className={styles.paramFund}>{def.fundamento}</span>}
        {alterado && <span className={styles.badgeAlterado}>alterado</span>}
      </label>
    );
  }

  return (
    <label className={`${styles.paramRange} ${alterado ? styles.paramAlterado : ''}`}>
      <span className={styles.paramRotulo}>
        {def.rotulo}
        <Ajuda texto={def.ajuda} />
        <strong className={styles.paramValor}>{formatValor(def, valor)}</strong>
        {alterado && <span className={styles.badgeAlterado}>alterado</span>}
      </span>
      {def.fundamento && <span className={styles.paramFund}>{def.fundamento}</span>}
      <input
        type="range"
        min={def.min ?? 0}
        max={def.max ?? 100}
        step={def.passo ?? 1}
        value={valor as number}
        onChange={(e) => onChange(Number(e.target.value))}
      />
    </label>
  );
}

export default function DetalheBeneficio({def, crimes: todos}: {def: BeneficioDef; crimes: Crime[]}) {
  // Benefícios se medem por patamar de pena: um tipo sem pena privativa cominada
  // satisfaria qualquer teto e apareceria como cabível em tudo.
  const crimes = useMemo(() => crimesComPenaPrivativa(todos), [todos]);
  const excluidos = todos.length - crimes.length;

  const [params, setParams] = useState<Parametros>(() => valoresPadrao(def));
  const [rev, setRev] = useState<CenarioReverso>(cenarioReversoPadrao);
  const [filtroStatus, setFiltroStatus] = useState<Status | 'todos'>('cabivel');
  const [q, setQ] = useState('');
  const [page, setPage] = useState(1);
  const urlTipos = useBaseUrl('/pesquisa/tipos');

  // Trocar de benefício sem desmontar o componente: recarrega os padrões.
  //
  // O filtro inicial acompanha a primeira faixa não vazia. Fixá-lo em "cabível"
  // abriria a tela com a tabela vazia nos benefícios que dependem de requisito
  // subjetivo — o ANPP, sem confissão marcada, não tem nenhum tipo cabível, só
  // condicionais.
  useEffect(() => {
    const padrao = valoresPadrao(def);
    const revPadrao = cenarioReversoPadrao();
    setParams(padrao);
    setRev(revPadrao);
    const c = contar(avaliarCatalogo(def, padrao, crimes, revPadrao));
    setFiltroStatus(c.cabivel > 0 ? 'cabivel' : c.condicional > 0 ? 'condicional' : 'todos');
    setQ('');
    setPage(1);
  }, [def.id, crimes]);

  const editado = foiEditado(def, params);
  const padroes = useMemo(() => valoresPadrao(def), [def.id]);

  const linhas = useMemo(
    () => avaliarCatalogo(def, params, crimes, rev),
    [def.id, params, crimes, rev],
  );
  const contagem = useMemo(() => contar(linhas), [linhas]);

  // Comparação com o estado legal vigente: quantos tipos o benefício alcança hoje?
  //
  // "Alcance" = tipos NÃO incabíveis. Medir só os `cabivel` daria um delta falso de
  // zero nos benefícios que dependem de requisito subjetivo: sem confissão marcada,
  // o ANPP nunca passa de `condicional`, e elevar seu teto de 4 para 8 anos — que
  // move 759 → 807 tipos — apareceria como "não mudou".
  const contagemPadrao = useMemo(
    () => contar(avaliarCatalogo(def, padroes, crimes, rev)),
    [def.id, padroes, crimes, rev],
  );
  const alcance = contagem.cabivel + contagem.condicional;
  const alcancePadrao = contagemPadrao.cabivel + contagemPadrao.condicional;
  const deltaAlcance = alcance - alcancePadrao;

  const visiveis = useMemo(() => {
    let out = linhas;
    if (filtroStatus !== 'todos') out = out.filter((l) => l.resultado.status === filtroStatus);
    if (q.trim()) {
      const termo = q.toLowerCase();
      out = out.filter(
        (l) =>
          l.crime.crime.toLowerCase().includes(termo) ||
          l.crime.artigo.toLowerCase().includes(termo) ||
          l.crime.lei.toLowerCase().includes(termo),
      );
    }
    return out;
  }, [linhas, filtroStatus, q]);

  const totalPages = Math.max(1, Math.ceil(visiveis.length / PAGE_SIZE));
  const pageClamped = Math.min(page, totalPages);
  const pageItems = visiveis.slice((pageClamped - 1) * PAGE_SIZE, pageClamped * PAGE_SIZE);

  const setParam = (id: string, v: number | boolean) => {
    setParams((p) => ({...p, [id]: v}));
    setPage(1);
  };
  const setRevCampo = <K extends keyof CenarioReverso>(k: K, v: CenarioReverso[K]) => {
    setRev((p) => ({...p, [k]: v}));
    setPage(1);
  };

  return (
    <div className={styles.detalhe}>
      <div className={styles.detalheHead}>
        <div>
          <h2 className={styles.detalheTitulo}>{def.nome}</h2>
          <div className={styles.detalheSub}>{def.fundamento}</div>
        </div>
        <div className={styles.detalheTags}>
          <span className={styles.tag}>{CATEGORIA_CURTA[def.categoria]}</span>
          <span className={`${styles.natTag} ${styles['nat_' + def.natureza]}`}>
            {NATUREZA_LABEL[def.natureza]}
          </span>
        </div>
      </div>

      <p className={styles.detalheDesc}>{def.descricao}</p>

      <div className={styles.reqVed}>
        <div className={styles.reqCol}>
          <h3 className={styles.colTitulo}>Requisitos</h3>
          <ul className={styles.listaReq}>
            {def.requisitos.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
        <div className={styles.reqCol}>
          <h3 className={styles.colTitulo}>Vedações</h3>
          {def.vedacoes.length > 0 ? (
            <ul className={styles.listaVed}>
              {def.vedacoes.map((v, i) => (
                <li key={i}>{v}</li>
              ))}
            </ul>
          ) : (
            <p className={styles.semVedacao}>Sem vedações legais específicas.</p>
          )}
        </div>
      </div>

      {/* ── Atributos editáveis do benefício ── */}
      <div className={styles.secao}>
        <h3 className={styles.secaoTitulo}>
          Atributos do benefício
          <Ajuda texto="Os valores partem da legislação vigente. Alterá-los simula uma reforma legal do próprio benefício — a lista de tipos penais afetados, abaixo, é recalculada imediatamente." />
          {editado && (
            <button className={styles.resetBtn} onClick={() => setParams(valoresPadrao(def))}>
              Restaurar valores legais
            </button>
          )}
        </h3>
        <p className={styles.secaoDica}>
          Cada atributo corresponde a um patamar, fração ou vedação extraída do dispositivo
          indicado. Os valores iniciais são os da <strong>legislação vigente</strong>.
        </p>
        <div className={styles.paramGrid}>
          {def.parametros.map((d) => (
            <ControleParametro
              key={d.id}
              def={d}
              valor={params[d.id]}
              padrao={d.padrao}
              onChange={(v) => setParam(d.id, v)}
            />
          ))}
        </div>
      </div>

      {/* ── Circunstâncias aplicadas a todo o catálogo ── */}
      <div className={styles.secao}>
        <h3 className={styles.secaoTitulo}>
          Circunstâncias do réu aplicadas ao catálogo
          <Ajuda texto="Ao contrário da busca por tipo penal, aqui as circunstâncias valem para TODOS os tipos ao mesmo tempo — é o que permite comparar o alcance do benefício sobre o catálogo inteiro." />
        </h3>

        {def.natureza === 'concreto' && (
          <div className={styles.pressuposto}>
            <strong>Pressuposto metodológico.</strong> Este benefício depende da pena fixada na
            sentença, que não é atributo do tipo penal. Para varrer o catálogo, o sistema presume
            uma pena concreta — por padrão, a <strong>pena mínima cominada</strong> (réu condenado
            no mínimo legal). Troque a base abaixo para testar outras hipóteses.
          </div>
        )}
        {def.natureza === 'abstrato' && (
          <div className={styles.pressupostoOk}>
            Este benefício depende apenas da <strong>pena cominada em abstrato</strong>: a
            avaliação de cada tipo penal é exata, sem presunção de pena concreta.
          </div>
        )}
        {def.natureza === 'incondicionado' && (
          <div className={styles.pressupostoOk}>
            Este benefício <strong>não depende de patamar de pena</strong> e alcança, em
            princípio, todo o catálogo. Os atributos acima descrevem sua forma de cálculo.
          </div>
        )}

        <div className={styles.circGrid}>
          <label className={styles.baseSelect}>
            <span>
              Pena concreta presumida
              <Ajuda texto={BASE_AJUDA[rev.base]} />
            </span>
            <select
              value={rev.base}
              onChange={(e) => setRevCampo('base', e.target.value as BasePenaConcreta)}>
              {(Object.keys(BASE_LABEL) as BasePenaConcreta[]).map((b) => (
                <option key={b} value={b}>
                  {BASE_LABEL[b]}
                </option>
              ))}
            </select>
          </label>

          {rev.base === 'fixa' && (
            <label className={styles.paramRange}>
              <span className={styles.paramRotulo}>
                Pena concreta fixa
                <strong className={styles.paramValor}>{formatPena(rev.penaFixaMeses)}</strong>
              </span>
              <input
                type="range"
                min={0}
                max={600}
                step={1}
                value={rev.penaFixaMeses}
                onChange={(e) => setRevCampo('penaFixaMeses', Number(e.target.value))}
              />
            </label>
          )}

          <div className={styles.checkGrid}>
            <label>
              <input
                type="checkbox"
                checked={rev.reincidenteEspecifico}
                onChange={(e) => setRevCampo('reincidenteEspecifico', e.target.checked)}
              />{' '}
              Reincidente específico
            </label>
            <label>
              <input
                type="checkbox"
                checked={rev.confessou}
                onChange={(e) => setRevCampo('confessou', e.target.checked)}
              />{' '}
              Confissão formal
            </label>
            <label>
              <input
                type="checkbox"
                checked={rev.reparouDano}
                onChange={(e) => setRevCampo('reparouDano', e.target.checked)}
              />{' '}
              Reparou o dano
            </label>
            <label>
              <input
                type="checkbox"
                checked={rev.bonsAntecedentes}
                onChange={(e) => setRevCampo('bonsAntecedentes', e.target.checked)}
              />{' '}
              Bons antecedentes
            </label>
          </div>
          <p className={styles.secaoDica}>
            Hediondez, violência, grave ameaça, culpa, resultado morte e previsão de perdão
            judicial <strong>não aparecem aqui</strong>: são atributos de cada tipo penal, lidos
            do catálogo dispositivo a dispositivo.
          </p>
        </div>
      </div>

      {/* ── Tipos penais afetados ── */}
      <div className={styles.secao}>
        <h3 className={styles.secaoTitulo}>
          Tipos penais afetados
          <span className={styles.totalTipos}>
            {crimes.length} tipos com pena privativa
            {excluidos > 0 && (
              <>
                {' '}
                <Ajuda
                  texto={`${excluidos} de ${todos.length} tipos penais do catálogo não cominam pena privativa de liberdade e ficam fora destas estatísticas, que se medem por patamar de pena — hoje, o art. 28 da Lei 11.343/06 (porte para consumo), cujas sanções são advertência, prestação de serviços e medida educativa. Eles continuam na Busca por tipo penal.`}
                />
              </>
            )}
          </span>
        </h3>

        <div className={styles.resumoGrid}>
          {(['cabivel', 'condicional', 'incabivel'] as Status[]).map((s) => (
            <button
              key={s}
              className={`${styles.resumoCard} ${styles['resumo_' + s]} ${
                filtroStatus === s ? styles.resumoAtivo : ''
              }`}
              onClick={() => {
                setFiltroStatus(s);
                setPage(1);
              }}>
              <span className={styles.resumoNum}>{contagem[s]}</span>
              <span className={styles.resumoLabel}>{STATUS_LABEL[s]}</span>
              <span className={styles.resumoPct}>
                {crimes.length > 0 ? ((contagem[s] / crimes.length) * 100).toFixed(1) : '0'}%
              </span>
            </button>
          ))}
          <button
            className={`${styles.resumoCard} ${filtroStatus === 'todos' ? styles.resumoAtivo : ''}`}
            onClick={() => {
              setFiltroStatus('todos');
              setPage(1);
            }}>
            <span className={styles.resumoNum}>{crimes.length}</span>
            <span className={styles.resumoLabel}>Todos</span>
            <span className={styles.resumoPct}>100%</span>
          </button>
        </div>

        {editado && (
          <div className={`${styles.delta} ${deltaAlcance === 0 ? styles.deltaNeutro : deltaAlcance > 0 ? styles.deltaMais : styles.deltaMenos}`}>
            {deltaAlcance === 0
              ? `Com os atributos alterados, o alcance do benefício não mudou: segue em ${alcance} de ${crimes.length} tipos penais.`
              : deltaAlcance > 0
                ? `Os atributos alterados AMPLIAM o alcance do benefício em ${deltaAlcance} ${deltaAlcance === 1 ? 'tipo penal' : 'tipos penais'} (de ${alcancePadrao} para ${alcance} de ${crimes.length}, contando cabíveis e condicionais).`
                : `Os atributos alterados REDUZEM o alcance do benefício em ${-deltaAlcance} ${-deltaAlcance === 1 ? 'tipo penal' : 'tipos penais'} (de ${alcancePadrao} para ${alcance} de ${crimes.length}, contando cabíveis e condicionais).`}
          </div>
        )}

        <div className={styles.searchBar}>
          <input
            className={styles.search}
            type="text"
            placeholder="Filtrar os tipos afetados por crime, artigo ou lei…"
            value={q}
            onChange={(e) => {
              setQ(e.target.value);
              setPage(1);
            }}
          />
          <span className={styles.count}>{visiveis.length} tipos listados</span>
        </div>

        <div className={styles.tableWrap}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Lei</th>
                <th>Artigo</th>
                <th>Crime</th>
                <th>Pena cominada</th>
                <th>Situação</th>
                <th>Fundamento do resultado</th>
              </tr>
            </thead>
            <tbody>
              {pageItems.map(({crime, resultado}) => (
                <tr key={crime.id}>
                  <td>{crime.lei}</td>
                  <td>{crime.artigo}</td>
                  <td>
                    <a
                      className={styles.linkTipo}
                      href={`${urlTipos}?tipo=${crime.id}`}
                      title="Abrir este tipo penal na busca por tipo penal">
                      {crime.crime}
                    </a>
                    {crime.hediondo === 'Sim' && <span className={styles.tagHed}>H</span>}
                  </td>
                  <td className={styles.penaCell}>{crime.pena_faixa_rotulo}</td>
                  <td>
                    <span className={`${styles.badge} ${styles['badge_' + resultado.status]}`}>
                      {STATUS_LABEL[resultado.status]}
                    </span>
                  </td>
                  <td className={styles.motivoCell}>{resultado.resumo}</td>
                </tr>
              ))}
              {pageItems.length === 0 && (
                <tr>
                  <td colSpan={6} className={styles.vazio}>
                    Nenhum tipo penal nessa situação com os filtros atuais.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {totalPages > 1 && (
          <div className={styles.pagination}>
            <button disabled={pageClamped === 1} onClick={() => setPage(pageClamped - 1)}>
              «
            </button>
            <span>
              Página {pageClamped} de {totalPages}
            </span>
            <button disabled={pageClamped === totalPages} onClick={() => setPage(pageClamped + 1)}>
              »
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

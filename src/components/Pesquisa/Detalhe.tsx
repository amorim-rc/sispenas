import React, {useEffect, useMemo, useState} from 'react';
import type {Crime, Cenario} from '@site/src/lib/types';
import {calcularBeneficios, CATEGORIA_LABEL, type Categoria, type BeneficioResultado} from '@site/src/lib/beneficios';
import {cenarioFromCrime} from '@site/src/lib/cenario';
import type {SelecaoModificador} from '@site/src/lib/dosimetria/types';
import {formatPena} from '@site/src/lib/format';
import Dosimetria from './Dosimetria';
import Concurso from './Concurso';
import ConcursoPessoas from './ConcursoPessoas';
import styles from './styles.module.css';

const STATUS_LABEL: Record<string, string> = {
  cabivel: 'Cabível',
  condicional: 'Condicional',
  incabivel: 'Incabível',
};

/**
 * Rótulo de um valor de pena em meses.
 *
 * `rotuloZero` existe porque zero significa coisas diferentes em cada controle:
 * na pena MÍNIMA quer dizer "sem mínimo cominado" — vários tipos só têm teto
 * ("detenção até 3 meses", art. 32 da LCP; arts. 289 e 309 do Código Eleitoral)
 * e continuam sendo puníveis. Chamá-los de "sem pena" seria falso.
 */
function meses(v: number, rotuloZero = 'sem pena'): string {
  if (v <= 0) return `0 meses (${rotuloZero})`;
  if (v < 1) return `${Math.round(v * 30)} dias`;
  const m = Math.round(v);
  const base = `${m} ${m === 1 ? 'mês' : 'meses'}`;
  const amigavel = formatPena(m);
  return amigavel === base ? base : `${base} (${amigavel})`;
}

function Ajuda({texto}: {texto: string}) {
  return (
    <span className={styles.ajuda} tabIndex={0} role="note" aria-label={texto} title={texto}>
      ?<span className={styles.ajudaBalao}>{texto}</span>
    </span>
  );
}

function BeneficioCard({b}: {b: BeneficioResultado}) {
  return (
    <div className={`${styles.benefCard} ${styles['status_' + b.status]}`}>
      <div className={styles.benefHead}>
        <span className={styles.benefNome}>{b.nome}</span>
        <span className={`${styles.benefBadge} ${styles['badge_' + b.status]}`}>{STATUS_LABEL[b.status]}</span>
      </div>
      <div className={styles.benefFund}>{b.fundamento}</div>
      <div className={styles.benefResumo}>{b.resumo}</div>
      {b.limiar && (
        <div className={styles.benefLimiar}>
          <span>{b.limiar.descricao}</span>
          <span className={b.limiar.folgaMeses >= 0 ? styles.folgaOk : styles.folgaNo}>
            {b.limiar.folgaMeses >= 0
              ? `folga de ${formatPena(b.limiar.folgaMeses)}`
              : `excede em ${formatPena(-b.limiar.folgaMeses)}`}
          </span>
        </div>
      )}
      <ul className={styles.benefDet}>
        {b.detalhes.map((d, i) => (
          <li key={i}>{d}</li>
        ))}
      </ul>
    </div>
  );
}

function artigoBase(artigo: string): string | null {
  const m = (artigo || '').match(/art\.?\s*(\d+(?:-[A-Za-z])?)/i);
  return m ? m[1].toLowerCase() : null;
}

export default function Detalhe({
  crime,
  todos,
  onSelect,
}: {
  crime: Crime;
  todos: Crime[];
  onSelect: (id: number) => void;
}) {
  const [cen, setCen] = useState<Cenario>(() => cenarioFromCrime(crime));

  const correlatos = useMemo(() => {
    const base = artigoBase(crime.artigo);
    if (!base) return [];
    return todos
      .filter((x) => x.id !== crime.id && x.lei === crime.lei && artigoBase(x.artigo) === base)
      .sort((a, b) => a.artigo.localeCompare(b.artigo, 'pt-BR', {numeric: true}));
  }, [crime.id, crime.artigo, crime.lei, todos]);

  useEffect(() => {
    setCen(cenarioFromCrime(crime));
  }, [crime.id]);

  // Seleção de modificadores erguida para cá: a dosimetria e o painel de
  // concurso de pessoas escrevem na MESMA lista, para que a participação de
  // menor importância entre no encadeamento das três fases — e não por fora.
  // Troca de tipo penal zera as escolhas: são do caso, não do catálogo.
  const [sel, setSel] = useState<SelecaoModificador[]>([]);
  useEffect(() => {
    setSel([]);
  }, [crime.id]);

  // Pena apurada na dosimetria por fases; null = nenhum modificador marcado,
  // e a barra manual de pena concreta segue no comando.
  const [penaDosimetria, setPenaDosimetria] = useState<number | null>(null);
  // Pena arrastada à mão na barra, guardada à parte para que o concurso possa
  // sobrepor-se sem destruí-la.
  const [penaManual, setPenaManual] = useState(() => cenarioFromCrime(crime).penaConcreta);
  useEffect(() => {
    setPenaManual(cenarioFromCrime(crime).penaConcreta);
  }, [crime.id]);

  // Pena do tipo EM FOCO, isolado — é ela que entra no concurso de crimes.
  // Não pode ser `cen.penaConcreta`, sob pena de realimentar o cálculo com o
  // próprio total cumulado.
  const penaIsolada = penaDosimetria ?? penaManual;

  // Pena cumulada da modalidade de concurso escolhida. Tem PRECEDÊNCIA sobre a
  // pena do tipo isolado: condenado em concurso, é o total que define o que o
  // réu pode pleitear.
  const [penaConcurso, setPenaConcurso] = useState<number | null>(null);

  useEffect(() => {
    setCen((p) => ({...p, penaConcreta: penaConcurso ?? penaIsolada}));
  }, [penaIsolada, penaConcurso]);

  const beneficios = useMemo(() => calcularBeneficios(cen), [cen]);
  const grupos: Categoria[] = ['processual', 'aplicacao', 'execucao'];

  const set = <K extends keyof Cenario>(k: K, v: Cenario[K]) => setCen((p) => ({...p, [k]: v}));

  const alteradoLegislativo =
    cen.penaMin !== crime.pena_min_meses || cen.penaMax !== crime.pena_max_meses;

  return (
    <div className={styles.detalhe}>
      <div className={styles.detalheHead}>
        <div>
          <h3 className={styles.detalheTitulo}>{crime.crime}</h3>
          <div className={styles.detalheSub}>
            {crime.artigo} · {crime.lei} · <strong>pena: {crime.pena_faixa_rotulo}</strong>
          </div>
        </div>
        <div className={styles.detalheTags}>
          <span className={styles.tag}>{crime.pena_privativa}</span>
          {crime.tem_multa && <span className={styles.tag}>Multa ({crime.multa_regime})</span>}
          {crime.hediondo === 'Sim' && <span className={`${styles.tag} ${styles.tagHed}`}>Hediondo</span>}
          {/* Classificação que depende do CASO, não do tipo: a etiqueta diz
              "pode ser", e a condição fica a um passar de mouse. Sem isso, o
              leitor veria "não hediondo" onde a lei diz "depende". */}
          {crime.hediondo_condicional && (
            <span className={`${styles.tag} ${styles.tagCondicional}`}>
              Hediondo se…
              <Ajuda texto={`A hediondez aqui depende de circunstância do caso, não do tipo. ${crime.hediondo_condicao} Marque "Hediondo/equiparado" nas circunstâncias abaixo para simular a hipótese.`} />
            </span>
          )}
          {/* Dispositivo que já não vige, e que continua no catálogo porque os
              fatos anteriores seguem regidos por ele. A etiqueta diz DESDE
              QUANDO; a nota diz o que houve e o que se aplica no lugar. */}
          {crime.vigente === false && (
            <span className={`${styles.tag} ${styles.tagNaoVigente}`}>
              Não vigente desde {crime.vigencia_ate}
              <Ajuda texto={`${crime.vigencia_nota} O registro permanece consultável: fatos anteriores a esta data continuam regidos por ele.`} />
            </span>
          )}
          <span className={styles.tag}>{crime.elemento}</span>
          <span className={styles.tag}>
            {crime.acao}
            {crime.acao_condicional && (
              <Ajuda texto={`A espécie de ação penal depende do caso. ${crime.acao_condicao}`} />
            )}
          </span>
        </div>
      </div>

      {crime.obs && <p className={styles.detalheObs}>{crime.obs}</p>}

      {/* Tipos sem pena privativa cominam sanções próprias (art. 28, I a III,
          da Lei 11.343/06). Sem isto, a tela diria apenas "sem pena privativa"
          e omitiria a consequência jurídica real do tipo. */}
      {crime.tem_pena_privativa === false && (crime.sancoes_nao_privativas ?? []).length > 0 && (
        <div className={styles.sancoes}>
          <h4 className={styles.sancoesTitulo}>
            Sanções cominadas
            <Ajuda texto="Este tipo penal não comina pena privativa de liberdade. Por isso os benefícios que dependem de patamar de pena (transação, ANPP, substituição, progressão) não lhe são aplicáveis, e ele fica fora das estatísticas de alcance da Busca por benefício." />
          </h4>
          <ul className={styles.sancoesLista}>
            {crime.sancoes_nao_privativas.map((s) => (
              <li key={s.inciso}>
                <span className={styles.sancaoInciso}>{s.inciso}</span> {s.sancao}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* O tipo que importa a moldura de outro dispositivo (art. 304 do CP:
          "pena cominada à falsificação") não tem número a exibir — mas tem de
          dizer ONDE a pena está, senão a tela sugere um crime sem pena. */}
      {crime.pena_por_remissao && (
        <div className={styles.sancoes}>
          <h4 className={styles.sancoesTitulo}>
            Pena por remissão
            <Ajuda texto="Este tipo não comina moldura própria: aplica a pena de outro dispositivo. Como a moldura depende de qual dispositivo-fonte incide no caso, o catálogo não publica um número — e o tipo fica fora das estatísticas de alcance da Busca por benefício." />
          </h4>
          <p>
            Aplica a pena cominada em <strong>{crime.pena_por_remissao.dispositivo_fonte}</strong>
            {crime.pena_por_remissao.operador !== 'nenhum' && crime.pena_por_remissao.fracao && (
              <>
                , com {crime.pena_por_remissao.operador === 'aumento' ? 'aumento' : 'diminuição'} de{' '}
                {crime.pena_por_remissao.fracao}
              </>
            )}
            .
          </p>
        </div>
      )}

      <div className={styles.simulador}>
        <div className={styles.simColuna}>
          <h4 className={styles.simTitulo}>Pena cominada — simulação legislativa</h4>
          <p className={styles.simDica}>
            Estas barras partem dos valores <strong>originais do tipo penal</strong>. Ajuste-as
            para estudar o impacto de uma alteração de pena sobre os benefícios.
          </p>
          <label className={styles.sliderRow}>
            <span>
              Pena mínima: <strong>{meses(cen.penaMin, 'sem mínimo cominado')}</strong>
              <Ajuda texto="Limite MÍNIMO de pena previsto na lei (pena em abstrato). Reduzi-lo até 0 permite testar a tese da ausência de pena mínima e ver quais benefícios processuais passam a caber (ex.: suspensão condicional do processo, ANPP)." />
            </span>
            <input type="range" min={0} max={480} step={1} value={cen.penaMin}
              onChange={(e) => set('penaMin', Math.min(+e.target.value, cen.penaMax))} />
          </label>
          <label className={styles.sliderRow}>
            <span>
              Pena máxima: <strong>{meses(cen.penaMax, 'sem teto cominado')}</strong>
              <Ajuda texto="Limite MÁXIMO de pena previsto na lei (pena em abstrato). Define, por exemplo, se o crime é de menor potencial ofensivo (até 2 anos) e o prazo de prescrição." />
            </span>
            <input type="range" min={0} max={600} step={1} value={cen.penaMax}
              onChange={(e) => set('penaMax', Math.max(+e.target.value, cen.penaMin))} />
          </label>
          <label className={styles.sliderRow}>
            <span>
              Pena concreta aplicada: <strong>{meses(cen.penaConcreta)}</strong>
              <Ajuda texto="Pena efetivamente fixada na sentença para um caso concreto (não é da lei, é da condenação). É a base dos benefícios de aplicação e execução: substituição por restritivas, sursis, regime inicial, progressão e livramento." />
              {penaConcurso !== null ? (
                <em className={styles.penaOrigem}>vinda do concurso de crimes</em>
              ) : penaDosimetria !== null ? (
                <em className={styles.penaOrigem}>vinda da dosimetria</em>
              ) : null}
            </span>
            <input type="range" min={0} max={600} step={1} value={cen.penaConcreta}
              onChange={(e) => setPenaManual(+e.target.value)} />
          </label>
          {alteradoLegislativo && (
            <button className={styles.resetBtn} onClick={() => setCen(cenarioFromCrime(crime))}>
              Restaurar pena original ({crime.pena_faixa_rotulo})
            </button>
          )}
        </div>

        <div className={styles.simColuna}>
          <h4 className={styles.simTitulo}>
            Circunstâncias do réu/caso
            <Ajuda texto="Marque as condições do caso concreto. Elas alteram as frações e vedações dos benefícios (ex.: reincidência muda a fração de progressão; violência/grave ameaça impede a substituição por restritivas)." />
          </h4>
          <div className={styles.checkGrid}>
            <label><input type="checkbox" checked={cen.primario} onChange={(e) => set('primario', e.target.checked)} /> Primário</label>
            <label><input type="checkbox" checked={cen.reincidenteEspecifico} onChange={(e) => set('reincidenteEspecifico', e.target.checked)} /> Reincidente específico</label>
            <label className={crime.hediondo_condicional ? styles.checkDestacado : undefined}>
              <input type="checkbox" checked={cen.hediondo} onChange={(e) => set('hediondo', e.target.checked)} />
              {' '}Hediondo/equiparado
              {crime.hediondo_condicional && <span className={styles.checkNota}> — depende do caso neste tipo</span>}
            </label>
            <label><input type="checkbox" checked={cen.resultadoMorte} onChange={(e) => set('resultadoMorte', e.target.checked)} /> Resultado morte</label>
            <label>
              <input type="checkbox" checked={cen.comandoOrgcrimUltraviolenta} onChange={(e) => set('comandoOrgcrimUltraviolenta', e.target.checked)} />
              {' '}Comando de facção
              <Ajuda texto={'Art. 112, VI, "b", da LEP, na redação da Lei 15.358/2026: condenado por exercer o comando, individual ou coletivo, de organização criminosa ultraviolenta estruturada para a prática de crime hediondo ou equiparado. Eleva a progressão a 75% e veda o livramento condicional. É circunstância do caso, não do tipo.'} />
            </label>
            <label><input type="checkbox" checked={cen.violencia} onChange={(e) => set('violencia', e.target.checked)} /> Violência</label>
            <label><input type="checkbox" checked={cen.graveAmeaca} onChange={(e) => set('graveAmeaca', e.target.checked)} /> Grave ameaça</label>
            <label><input type="checkbox" checked={cen.confessou} onChange={(e) => set('confessou', e.target.checked)} /> Confissão formal</label>
            <label><input type="checkbox" checked={cen.bonsAntecedentes} onChange={(e) => set('bonsAntecedentes', e.target.checked)} /> Bons antecedentes</label>
            <label><input type="checkbox" checked={cen.culposo} onChange={(e) => set('culposo', e.target.checked)} /> Culposo</label>
            <label>
              <input type="checkbox" checked={cen.fatoAnteriorA15402} onChange={(e) => set('fatoAnteriorA15402', e.target.checked)} />
              {' '}Fato anterior a 08/05/2026
              <Ajuda texto={'A Lei 15.402/2026 reescreveu o caput e os incisos I a III do art. 112 da LEP. Para o primário condenado por crime SEM violência ela é mais gravosa — os 16% do inciso I viraram 1/6 do caput, que é 16,67% —, e lei mais gravosa não retroage. Marque para calcular pela tabela do Pacote Anticrime, que é a lei do fato anterior.'} />
            </label>
            <label><input type="checkbox" checked={cen.reparouDano} onChange={(e) => set('reparouDano', e.target.checked)} /> Reparou o dano</label>
          </div>
        </div>
      </div>

      <Dosimetria
        crime={crime}
        penaMin={cen.penaMin}
        penaMax={cen.penaMax}
        sel={sel}
        setSel={setSel}
        onPenaDefinitiva={setPenaDosimetria}
      />

      {crime.tem_pena_privativa && (
        <div className={styles.concursosGrid}>
          <Concurso
            crime={crime}
            penaAtual={penaIsolada}
            todos={todos}
            onPenaConcurso={setPenaConcurso}
          />
          <ConcursoPessoas sel={sel} setSel={setSel} />
        </div>
      )}

      <h4 className={styles.benefSecTitulo}>Benefícios penais — recálculo dinâmico</h4>
      {grupos.map((g) => (
        <div key={g} className={styles.benefGrupo}>
          <div className={styles.benefGrupoTitulo}>{CATEGORIA_LABEL[g]}</div>
          <div className={styles.benefGrid}>
            {beneficios.filter((b) => b.categoria === g).map((b) => (
              <BeneficioCard key={b.id} b={b} />
            ))}
          </div>
        </div>
      ))}

      {correlatos.length > 0 && (
        <div className={styles.correlatos}>
          <h4 className={styles.benefSecTitulo}>
            Tipos correlatos
            <Ajuda texto="Outros dispositivos do mesmo artigo-base na mesma lei (parágrafos, incisos, formas qualificadas/privilegiadas). Clique para carregar o cálculo do dispositivo." />
          </h4>
          <div className={styles.correlatosLista}>
            {correlatos.map((x) => {
              const duplicata = x.artigo === crime.artigo;
              return (
                <button key={x.id} className={styles.correlatoItem} onClick={() => onSelect(x.id)}>
                  <span className={styles.correlatoArtigo}>{x.artigo}</span>
                  <span className={styles.correlatoCrime}>{x.crime}</span>
                  <span className={styles.correlatoPena}>{x.pena_faixa_rotulo}</span>
                  {duplicata && <span className={styles.correlatoDup} title="Mesmo artigo do tipo selecionado — possível duplicata a revisar">possível duplicata</span>}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

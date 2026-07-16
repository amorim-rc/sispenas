import React, {useEffect, useMemo, useState} from 'react';
import type {Crime, Cenario} from '@site/src/lib/types';
import {calcularBeneficios, CATEGORIA_LABEL, type Categoria, type BeneficioResultado} from '@site/src/lib/beneficios';
import {cenarioFromCrime} from '@site/src/lib/cenario';
import {formatPena} from '@site/src/lib/format';
import styles from './styles.module.css';

const STATUS_LABEL: Record<string, string> = {
  cabivel: 'Cabível',
  condicional: 'Condicional',
  incabivel: 'Incabível',
};

function meses(v: number): string {
  if (v <= 0) return '0 meses (sem pena)';
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
          <span className={styles.tag}>{crime.elemento}</span>
          <span className={styles.tag}>{crime.acao}</span>
        </div>
      </div>

      {crime.obs && <p className={styles.detalheObs}>{crime.obs}</p>}

      <div className={styles.simulador}>
        <div className={styles.simColuna}>
          <h4 className={styles.simTitulo}>Pena cominada — simulação legislativa</h4>
          <p className={styles.simDica}>
            Estas barras partem dos valores <strong>originais do tipo penal</strong>. Ajuste-as
            para estudar o impacto de uma alteração de pena sobre os benefícios.
          </p>
          <label className={styles.sliderRow}>
            <span>
              Pena mínima: <strong>{meses(cen.penaMin)}</strong>
              <Ajuda texto="Limite MÍNIMO de pena previsto na lei (pena em abstrato). Reduzi-lo até 0 permite testar a tese da ausência de pena mínima e ver quais benefícios processuais passam a caber (ex.: suspensão condicional do processo, ANPP)." />
            </span>
            <input type="range" min={0} max={480} step={1} value={cen.penaMin}
              onChange={(e) => set('penaMin', Math.min(+e.target.value, cen.penaMax))} />
          </label>
          <label className={styles.sliderRow}>
            <span>
              Pena máxima: <strong>{meses(cen.penaMax)}</strong>
              <Ajuda texto="Limite MÁXIMO de pena previsto na lei (pena em abstrato). Define, por exemplo, se o crime é de menor potencial ofensivo (até 2 anos) e o prazo de prescrição." />
            </span>
            <input type="range" min={0} max={600} step={1} value={cen.penaMax}
              onChange={(e) => set('penaMax', Math.max(+e.target.value, cen.penaMin))} />
          </label>
          <label className={styles.sliderRow}>
            <span>
              Pena concreta aplicada: <strong>{meses(cen.penaConcreta)}</strong>
              <Ajuda texto="Pena efetivamente fixada na sentença para um caso concreto (não é da lei, é da condenação). É a base dos benefícios de aplicação e execução: substituição por restritivas, sursis, regime inicial, progressão e livramento." />
            </span>
            <input type="range" min={0} max={600} step={1} value={cen.penaConcreta}
              onChange={(e) => set('penaConcreta', +e.target.value)} />
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
            <label><input type="checkbox" checked={cen.hediondo} onChange={(e) => set('hediondo', e.target.checked)} /> Hediondo/equiparado</label>
            <label><input type="checkbox" checked={cen.resultadoMorte} onChange={(e) => set('resultadoMorte', e.target.checked)} /> Resultado morte</label>
            <label><input type="checkbox" checked={cen.violencia} onChange={(e) => set('violencia', e.target.checked)} /> Violência</label>
            <label><input type="checkbox" checked={cen.graveAmeaca} onChange={(e) => set('graveAmeaca', e.target.checked)} /> Grave ameaça</label>
            <label><input type="checkbox" checked={cen.confessou} onChange={(e) => set('confessou', e.target.checked)} /> Confissão formal</label>
            <label><input type="checkbox" checked={cen.bonsAntecedentes} onChange={(e) => set('bonsAntecedentes', e.target.checked)} /> Bons antecedentes</label>
            <label><input type="checkbox" checked={cen.culposo} onChange={(e) => set('culposo', e.target.checked)} /> Culposo</label>
            <label><input type="checkbox" checked={cen.reparouDano} onChange={(e) => set('reparouDano', e.target.checked)} /> Reparou o dano</label>
          </div>
        </div>
      </div>

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

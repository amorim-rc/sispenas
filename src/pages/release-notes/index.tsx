// Notas de atualizações — feed de mudanças no padrão EBANX.
//
// Lê o array agregado de src/data/changelog (require.context sobre os arquivos
// .ts, um por entrada). Substitui o antigo blog do Docusaurus: aqui cada entrada
// é uma mudança, não uma versão inteira, filtrável por Tipo, Área e Versão.

import {useMemo, useState} from 'react';
import Layout from '@theme/Layout';

import entries from '@site/src/data/changelog';
import type {ChangelogArea, ChangelogTipo} from '@site/src/data/changelog/types';

import '@fontsource/inter/400.css';
import '@fontsource/inter/500.css';
import '@fontsource/inter/600.css';
import '@fontsource/inter/700.css';
import styles from './styles.module.css';

const TIPOS: {valor: ChangelogTipo; rotulo: string}[] = [
  {valor: 'novidade', rotulo: 'Novidade'},
  {valor: 'melhoria', rotulo: 'Melhoria'},
  {valor: 'correcao', rotulo: 'Correção'},
  {valor: 'estrutural', rotulo: 'Estrutural'},
];
const TIPO_ROTULO: Record<ChangelogTipo, string> = {
  novidade: 'Novidade',
  melhoria: 'Melhoria',
  correcao: 'Correção',
  estrutural: 'Estrutural',
};
const AREAS: ChangelogArea[] = [
  'Tipos penais',
  'Benefícios',
  'Dosimetria',
  'Acervo histórico',
  'Interface',
  'Documentação',
];
const AREA_SLUG: Record<ChangelogArea, string> = {
  'Tipos penais': 'tipos-penais',
  'Benefícios': 'beneficios',
  Dosimetria: 'dosimetria',
  'Acervo histórico': 'acervo',
  Interface: 'interface',
  Documentação: 'documentacao',
};
const MESES = [
  'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
  'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro',
];

function formatarData(iso: string): string {
  const [a, m, d] = iso.split('-').map(Number);
  return `${d} de ${MESES[m - 1]} de ${a}`;
}

function useToggleSet() {
  const [set, setSet] = useState<Set<string>>(new Set());
  const toggle = (v: string) =>
    setSet((prev) => {
      const nova = new Set(prev);
      if (nova.has(v)) nova.delete(v);
      else nova.add(v);
      return nova;
    });
  const limpar = () => setSet(new Set());
  return {set, toggle, limpar};
}

export default function NotasDeAtualizacoes() {
  const tipo = useToggleSet();
  const area = useToggleSet();
  const versao = useToggleSet();
  const [menuAberto, setMenuAberto] = useState(false);

  const versoes = useMemo(() => {
    const vistos: string[] = [];
    for (const e of entries) {
      if (e.version && !vistos.includes(e.version)) vistos.push(e.version);
    }
    return vistos;
  }, []);

  const visiveis = useMemo(
    () =>
      entries.filter((e) => {
        const okTipo = tipo.set.size === 0 || tipo.set.has(e.tipo);
        const okArea = area.set.size === 0 || e.areas.some((a) => area.set.has(a));
        const okVersao =
          versao.set.size === 0 || (e.version != null && versao.set.has(e.version));
        return okTipo && okArea && okVersao;
      }),
    [tipo.set, area.set, versao.set],
  );

  const ativos = tipo.set.size + area.set.size + versao.set.size;
  const limparTudo = () => {
    tipo.limpar();
    area.limpar();
    versao.limpar();
  };

  return (
    <Layout
      title="Notas de atualizações"
      description="O que muda no catálogo, nos benefícios e na ferramenta do SISPENAS — cada alteração datada e resumida.">
      <div className={styles.pagina}>
        <div className={styles.wrap}>
          <header className={styles.cabecalho}>
            <h1 className={styles.h1}>Notas de atualizações</h1>
            <p className={styles.lede}>
              O que muda no catálogo, nos benefícios e na ferramenta — cada alteração
              datada, resumida em um parágrafo e aberta em detalhe quando você quiser.
            </p>
          </header>

          <div className={styles.layout}>
            <button
              className={styles.filtrosToggle}
              aria-expanded={menuAberto}
              aria-controls="filtros-menu"
              onClick={() => setMenuAberto((v) => !v)}>
              <span>Filtros</span>
              {ativos > 0 && <span className={styles.badge}>{ativos}</span>}
              <span className={styles.tchev} aria-hidden>▾</span>
            </button>

            <aside
              id="filtros-menu"
              className={`${styles.filtros} ${menuAberto ? styles.aberto : ''}`}
              aria-label="Filtros">
              <p className={styles.filtrosTitulo}>Filtros</p>

              <div className={styles.grupo}>
                <p className={styles.grupoRotulo}>Tipo</p>
                {TIPOS.map((t) => (
                  <label key={t.valor} className={styles.opcao}>
                    <input
                      type="checkbox"
                      checked={tipo.set.has(t.valor)}
                      onChange={() => tipo.toggle(t.valor)}
                    />
                    {t.rotulo}
                  </label>
                ))}
              </div>

              <div className={styles.grupo}>
                <p className={styles.grupoRotulo}>Área</p>
                {AREAS.map((a) => (
                  <label key={a} className={styles.opcao}>
                    <input
                      type="checkbox"
                      checked={area.set.has(a)}
                      onChange={() => area.toggle(a)}
                    />
                    {a}
                  </label>
                ))}
              </div>

              <div className={styles.grupo}>
                <p className={styles.grupoRotulo}>Versão</p>
                {versoes.map((v) => (
                  <label key={v} className={styles.opcao}>
                    <input
                      type="checkbox"
                      checked={versao.set.has(v)}
                      onChange={() => versao.toggle(v)}
                    />
                    {v}
                  </label>
                ))}
              </div>

              <button className={styles.limpar} disabled={ativos === 0} onClick={limparTudo}>
                Limpar filtros
              </button>
            </aside>

            <main>
              <p className={styles.contagem}>
                {visiveis.length} {visiveis.length === 1 ? 'registro' : 'registros'}
              </p>
              {visiveis.length === 0 ? (
                <p className={styles.vazio}>
                  Nenhuma entrada corresponde aos filtros selecionados.
                </p>
              ) : (
                <ul className={styles.lista}>
                  {visiveis.map((e) => (
                    <li key={e.id} className={styles.entrada}>
                      <p className={styles.data}>{formatarData(e.date)}</p>
                      <h2 className={styles.titulo}>{e.title}</h2>
                      <p className={styles.resumo}>{e.summary}</p>
                      <div className={styles.tags}>
                        <span
                          className={`${styles.tag} ${styles.tagTipo}`}
                          data-tipo={e.tipo}>
                          {TIPO_ROTULO[e.tipo]}
                        </span>
                        {e.areas.map((a) => (
                          <span
                            key={a}
                            className={`${styles.tag} ${styles.tagArea}`}
                            data-slug={AREA_SLUG[a]}>
                            {a}
                          </span>
                        ))}
                        {e.version && (
                          <span className={`${styles.tag} ${styles.tagVersao}`}>
                            {e.version}
                          </span>
                        )}
                      </div>
                      {(e.body.length > 0 || (e.links && e.links.length > 0)) && (
                        <details className={styles.detalhe}>
                          <summary>
                            <span className={styles.chevron} aria-hidden>›</span> Abrir detalhes
                          </summary>
                          <div className={styles.corpo}>
                            {e.body.map((p, i) => (
                              <p key={i}>{p}</p>
                            ))}
                            {e.links && e.links.length > 0 && (
                              <div className={styles.links}>
                                {e.links.map((l) => (
                                  <a key={l.href} className={styles.linkLocal} href={l.href}>
                                    {l.label} <span className={styles.setaLink} aria-hidden>→</span>
                                  </a>
                                ))}
                              </div>
                            )}
                          </div>
                        </details>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </main>
          </div>
        </div>
      </div>
    </Layout>
  );
}

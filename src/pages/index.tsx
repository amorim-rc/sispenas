import {useEffect, type ReactNode} from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import useBaseUrl from '@docusaurus/useBaseUrl';
import BrowserOnly from '@docusaurus/BrowserOnly';

import styles from './index.module.css';

/**
 * Até a v1.0.0 a pesquisa de tipos penais era servida na raiz e o tipo
 * selecionado vinha em `/?tipo=N`. A raiz passou a ser a landing page, então
 * esses links (já publicados e indexados) são reencaminhados para a nova rota.
 */
function RedirecionaLinksAntigos(): null {
  const destino = useBaseUrl('/pesquisa/tipos');
  useEffect(() => {
    const tipo = new URLSearchParams(window.location.search).get('tipo');
    if (tipo) window.location.replace(`${destino}?tipo=${encodeURIComponent(tipo)}`);
  }, [destino]);
  return null;
}

function Hero() {
  return (
    <header className={styles.hero}>
      <div className="container">
        <Heading as="h1" className={styles.heroTitle}>SISPENAS</Heading>
        <p className={styles.heroSub}>
          Sistema de Pesquisa de Tipos Penais e Benefícios
        </p>
        <p className={styles.heroNote}>
          Ferramenta aberta para estudar o impacto dos benefícios penais sobre os tipos
          penais brasileiros — e o efeito de alterações de pena sobre o acesso a eles.
        </p>
      </div>
    </header>
  );
}

function Caminhos() {
  return (
    <section className={styles.caminhos}>
      <div className="container">
        <div className={styles.caminhosGrid}>
          <Link className={styles.caminhoCard} to="/pesquisa/tipos">
            <h3>Busca por tipo penal</h3>
            <p>
              Parte de um crime e mostra a dosimetria padrão e todos os benefícios penais
              cabíveis. Ajuste a pena cominada ou a pena concreta e veja, em tempo real,
              quais benefícios entram ou saem.
            </p>
          </Link>
          <Link className={styles.caminhoCard} to="/pesquisa/beneficios">
            <h3>Busca por benefício</h3>
            <p>
              Parte de um benefício, expõe seus requisitos, vedações e patamares legais — e
              lista os tipos penais que ele alcança. Altere qualquer atributo do benefício e
              veja o catálogo inteiro se reorganizar.
            </p>
          </Link>
        </div>
      </div>
    </section>
  );
}

function Sobre() {
  return (
    <section className={styles.sobre}>
      <div className="container">
        <div className={styles.sobreCorpo}>
          <Heading as="h2" id="sobre-o-sispenas">Sobre o SISPENAS</Heading>

          <p>
            O <strong>SISPENAS</strong> (Sistema de Pesquisa de Tipos Penais e Benefícios) é
            uma ferramenta aberta de <strong>pesquisa de políticas públicas</strong> cujo
            objetivo central é estudar o <strong>impacto dos benefícios penais</strong> sobre
            os tipos penais brasileiros.
          </p>

          <p>A partir de um catálogo estruturado de tipos penais, a ferramenta permite:</p>

          <ul>
            <li>
              <strong>Pesquisar</strong> tipos penais por nome, artigo, diploma legislativo ou
              benefício aplicável;
            </li>
            <li>
              <strong>Filtrar</strong> por múltiplas dimensões — modalidade de pena (reclusão,
              detenção, prisão simples, multa), hediondez, elemento subjetivo, violência/grave
              ameaça, ação penal, infração de menor potencial ofensivo — de forma{' '}
              <strong>combinada ou isolada</strong>;
            </li>
            <li>
              <strong>Simular</strong> alterações de pena e observar, <strong>dinamicamente</strong>,
              como cada benefício penal se torna cabível ou incabível;
            </li>
            <li>
              <strong>Inverter o percurso</strong>: partir de um benefício penal, editar seus
              patamares, frações e vedações, e observar quais tipos penais passam a ser
              alcançados.
            </li>
          </ul>

          <Heading as="h3" id="vocacao">Vocação</Heading>
          <p>
            O SISPENAS é orientado à <strong>pesquisa acadêmica, legislativa e de políticas
            públicas</strong>. A pergunta que ele ajuda a responder é: <em>o que muda no acesso
            a benefícios penais quando uma pena é alterada?</em> Ao tornar visível a relação
            entre patamares de pena e os limiares legais dos benefícios (ANPP, transação penal,
            substituição, sursis, progressão, livramento, prescrição, etc.), a ferramenta apoia
            o desenho e a crítica de propostas legislativas.
          </p>

          <Heading as="h3" id="origem">Origem</Heading>
          <p>
            O SISPENAS tem origem na pesquisa coordenada pelas professoras{' '}
            <strong>Maíra Rocha Machado</strong> e <strong>Marta Rodriguez de Assis
            Machado</strong> (Escola de Direito da Fundação Getúlio Vargas — Direito GV), que
            conceberam o <strong>SISPENAS</strong> como um sistema de consulta sobre crimes,
            penas e alternativas à prisão. A referência seminal do projeto é:
          </p>

          <blockquote>
            <p>
              MACHADO, Maíra Rocha; MACHADO, Marta Rodriguez de Assis (coord.).{' '}
              <strong>SISPENAS: Sistema de Consulta sobre Crimes, Penas e Alternativas à
              Prisão</strong>. Revista Jurídica, Brasília, v. 10, n. 90, ed. esp., p. 1-26,
              abr./maio 2008.
            </p>
            <p>
              Íntegra:{' '}
              <Link to="pathname:///sispenas/artigos/machado-machado-2008-sispenas-rev-juridica-90.pdf">
                artigo original (PDF)
              </Link>
              .
            </p>
          </blockquote>

          <p>
            O SISPENAS original foi um projeto de pesquisa vinculado a edital da Secretaria de
            Assuntos Legislativos do Ministério da Justiça, com o objetivo de enfrentar o{' '}
            <strong>déficit de informação pública</strong> sobre o sistema penal: tornar visível
            e pesquisável a relação entre os <strong>tipos penais</strong> e os{' '}
            <strong>benefícios/alternativas à prisão</strong>, e permitir <strong>simular</strong>{' '}
            o efeito de alterações legislativas.
          </p>

          <p>
            Esta plataforma é uma <strong>reimplementação digital, aberta e interativa</strong>{' '}
            dessa proposta: preserva a intuição original — catalogar exaustivamente os tipos
            penais e cruzá-los com os benefícios — e a atualiza para a legislação vigente, com
            simulação dinâmica de pena e dados abertos. A comparação detalhada entre a proposta
            de 2008 e esta implementação está no <code>README.md</code> do repositório.
          </p>

          <Heading as="h3" id="aviso-importante">Aviso importante</Heading>
          <div className={styles.aviso}>
            <p>
              Esta é uma ferramenta de <strong>pesquisa</strong>. Os cálculos simplificam
              controvérsias doutrinárias e jurisprudenciais e{' '}
              <strong>não constituem aconselhamento jurídico</strong>. Parte significativa dos
              dados foi derivada automaticamente a partir do texto legal e ainda será revisada
              individualmente.
            </p>
          </div>

          <Heading as="h3" id="creditos">Créditos</Heading>
          <p>
            Desenvolvido pela <strong>Equipe SISPENAS</strong>. Licença MIT com atribuição.
          </p>

          <p className={styles.sobreLinks}>
            <Link to="/docs/metodologia">Metodologia</Link>
            {' · '}
            <Link to="/docs/beneficios-penais">Benefícios penais</Link>
            {' · '}
            <Link to="/docs/dados-abertos">Dados abertos</Link>
            {' · '}
            <Link to="/docs/roadmap">Roadmap</Link>
          </p>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  return (
    <Layout
      title="Sobre o SISPENAS"
      description="SISPENAS — sistema de pesquisa de tipos penais brasileiros e estudo dinâmico do impacto dos benefícios penais para pesquisa de políticas públicas.">
      <BrowserOnly>{() => <RedirecionaLinksAntigos />}</BrowserOnly>
      <Hero />
      <main>
        <Caminhos />
        <Sobre />
      </main>
    </Layout>
  );
}

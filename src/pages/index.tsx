import type {ReactNode} from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Pesquisa from '@site/src/components/Pesquisa';

import styles from './index.module.css';

function Header() {
  return (
    <header className={styles.hero}>
      <div className="container">
        <Heading as="h1" className={styles.heroTitle}>SISPENAS</Heading>
        <p className={styles.heroSub}>
          Sistema de pesquisa de tipos penais brasileiros e estudo do impacto dos benefícios penais.
        </p>
        <p className={styles.heroNote}>
          Busque por nome, artigo, lei ou benefício. Selecione um tipo para simular alterações de
          pena e ver, em tempo real, quais benefícios penais se tornam cabíveis ou incabíveis.
        </p>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  return (
    <Layout
      title="Pesquisa de tipos penais e benefícios"
      description="SISPENAS — catálogo de tipos penais brasileiros e estudo dinâmico do impacto dos benefícios penais para pesquisa de políticas públicas.">
      <Header />
      <main>
        <Pesquisa />
      </main>
    </Layout>
  );
}

import type {ReactNode} from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Pesquisa from '@site/src/components/Pesquisa';
import Citacao from '@site/src/components/Citacao';

import styles from './pesquisa.module.css';

export default function BuscaPorTipoPenal(): ReactNode {
  return (
    <Layout
      title="Busca por tipo penal"
      description="Catálogo de tipos penais brasileiros com dosimetria padrão e cálculo dinâmico dos benefícios penais aplicáveis.">
      <header className={styles.cabecalho}>
        <div className="container">
          <Heading as="h1" className={styles.titulo}>Busca por tipo penal</Heading>
          <p className={styles.subtitulo}>
            Busque por nome, artigo, lei ou benefício. Selecione um tipo para ver a dosimetria
            padrão, simular alterações de pena e observar, em tempo real, quais benefícios
            penais se tornam cabíveis ou incabíveis.
          </p>
        </div>
      </header>
      <main>
        <Pesquisa />
        <div className="container">
          <Citacao compacto />
        </div>
      </main>
    </Layout>
  );
}

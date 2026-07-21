import type {ReactNode} from 'react';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import BuscaBeneficio from '@site/src/components/BuscaBeneficio';
import Citacao from '@site/src/components/Citacao';

import styles from './pesquisa.module.css';

export default function BuscaPorBeneficio(): ReactNode {
  return (
    <Layout
      title="Busca por benefício"
      description="Catálogo de benefícios penais brasileiros: requisitos, vedações e patamares legais editáveis, com a lista dos tipos penais alcançados.">
      <header className={styles.cabecalho}>
        <div className="container">
          <Heading as="h1" className={styles.titulo}>Busca por benefício</Heading>
          <p className={styles.subtitulo}>
            O percurso inverso: parta de um benefício penal, examine seus requisitos, vedações
            e patamares legais — e veja quais tipos penais ele alcança. Altere qualquer atributo
            do benefício e a lista de tipos afetados é recalculada na hora.
          </p>
        </div>
      </header>
      <main>
        <BuscaBeneficio />
        <div className="container">
          <Citacao compacto />
        </div>
      </main>
    </Layout>
  );
}

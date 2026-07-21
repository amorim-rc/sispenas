import {useState, type ReactNode} from 'react';
import Link from '@docusaurus/Link';

import styles from './styles.module.css';

const SITE = 'https://amorim-rc.github.io/sispenas/';

/** Data de acesso no formato ABNT (ex.: "21 jul. 2026"). */
function dataAcesso(): string {
  const meses = ['jan.', 'fev.', 'mar.', 'abr.', 'maio', 'jun.',
                 'jul.', 'ago.', 'set.', 'out.', 'nov.', 'dez.'];
  const d = new Date();
  return `${d.getDate()} ${meses[d.getMonth()]} ${d.getFullYear()}`;
}

/**
 * Bloco "Como citar" — reiterado na página inicial e nas telas de pesquisa,
 * para que o uso acadêmico seja simples e o sistema, mais citado. A referência
 * canônica em CITATION.cff (BibTeX/CFF) fica linkada em Dados abertos.
 */
export default function Citacao({compacto = false}: {compacto?: boolean}): ReactNode {
  const [copiado, setCopiado] = useState(false);
  const texto =
    `EQUIPE SISPENAS. SISPENAS: Sistema de Pesquisa de Tipos Penais e Benefícios. ` +
    `Disponível em: ${SITE}. Acesso em: ${dataAcesso()}.`;

  function copiar() {
    navigator.clipboard?.writeText(texto).then(
      () => {
        setCopiado(true);
        setTimeout(() => setCopiado(false), 2000);
      },
      () => {},
    );
  }

  return (
    <aside className={`${styles.citacao} ${compacto ? styles.compacto : ''}`} aria-label="Como citar">
      <div className={styles.cabecalho}>
        <h3 className={styles.titulo}>Como citar</h3>
        <button type="button" className={styles.botao} onClick={copiar}>
          {copiado ? 'Copiado ✓' : 'Copiar'}
        </button>
      </div>
      <p className={styles.referencia}>{texto}</p>
      <p className={styles.origem}>
        Reimplementação do sistema concebido por MACHADO, Maíra Rocha; MACHADO, Marta
        Rodriguez de Assis. <em>SISPENAS: Sistema de Consulta sobre Crimes, Penas e
        Alternativas à Prisão</em>. Revista Jurídica, Brasília, v. 10, n. 90, p. 1–26, 2008.
      </p>
      <p className={styles.formatos}>
        Formatos BibTeX e CFF em <Link to="/docs/dados-abertos#como-citar">Dados abertos</Link>.
      </p>
    </aside>
  );
}

import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// "Sobre o SISPENAS" vive na landing page (src/pages/index.tsx) e o Roadmap é
// página única, acessada direto pela navbar — por isso nenhum dos dois compõe
// esta barra lateral.
const sidebars: SidebarsConfig = {
  docsSidebar: [
    'metodologia',
    'catalogo-tipos-penais',
    'beneficios-penais',
    'dados-abertos',
  ],
};

export default sidebars;

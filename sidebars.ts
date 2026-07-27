import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// "Sobre o SISPENAS" vive na landing page (src/pages/index.tsx) e o Roadmap é
// página única, acessada direto pela navbar — por isso nenhum dos dois compõe
// esta barra lateral. O "Acervo histórico" também não: é página própria,
// acessada pelo menu Pesquisa (ainda em /docs/acervo-historico, fora da sidebar).
const sidebars: SidebarsConfig = {
  docsSidebar: [
    'metodologia',
    'completude',
    'catalogo-tipos-penais',
    'beneficios-penais',
    'dados-abertos',
  ],
};

export default sidebars;

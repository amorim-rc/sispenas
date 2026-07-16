import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'SISPENAS',
  tagline: 'Sistema de Pesquisa de Tipos Penais e Benefícios — Brasil',
  favicon: 'img/favicon.svg',

  future: {
    v4: true,
  },

  url: 'https://amorim-rc.github.io',
  baseUrl: '/sispenas/',

  organizationName: 'amorim-rc',
  projectName: 'sispenas',

  onBrokenLinks: 'warn',

  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  i18n: {
    defaultLocale: 'pt-BR',
    locales: ['pt-BR'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: 'docs',
        },
        // O plugin de blog serve de changelog: cada release é um post datado em
        // release-notes/. É a mesma abordagem que o próprio Docusaurus usa para
        // o changelog dele. O roadmap fica só com o que está por vir.
        blog: {
          path: 'release-notes',
          routeBasePath: 'release-notes',
          blogTitle: 'Release notes',
          blogDescription: 'Histórico de versões do SISPENAS.',
          blogSidebarTitle: 'Versões',
          blogSidebarCount: 'ALL',
          showReadingTime: false,
          onUntruncatedBlogPosts: 'ignore',
          feedOptions: {
            type: 'all',
            title: 'SISPENAS — Release notes',
            copyright: `SISPENAS © ${new Date().getFullYear()} — Equipe SISPENAS.`,
          },
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-client-redirects',
      {
        // Até a v1.0.0, "Sobre o SISPENAS" era uma página da documentação e a
        // pesquisa de tipos penais era servida na raiz. Ambas mudaram de lugar na
        // v1.1.0; estes redirecionamentos preservam os links já publicados.
        // O caso `/?tipo=N` depende da query string e é tratado em src/pages/index.tsx.
        redirects: [
          {from: '/docs/sobre', to: '/'},
        ],
      },
    ],
  ],

  themeConfig: {
    // `image` (og:image) fica de fora até existir um social card próprio: apontava
    // para img/sispenas-social-card.jpg, que nunca existiu no repositório — o
    // arquivo presente era o card padrão do Docusaurus, com outro nome. Uma
    // referência quebrada é pior que a ausência: o og:image 404 aparece como
    // imagem falha no compartilhamento. Ver roadmap (melhorias transversais).
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'SISPENAS',
      logo: {
        alt: 'SISPENAS',
        src: 'img/logo.svg',
      },
      items: [
        {to: '/', label: 'Sobre o SISPENAS', position: 'left', activeBaseRegex: '^/sispenas/$'},
        {
          type: 'dropdown',
          label: 'Pesquisa',
          position: 'left',
          items: [
            {to: '/pesquisa/tipos', label: 'Busca por tipo penal'},
            {to: '/pesquisa/beneficios', label: 'Busca por benefício'},
          ],
        },
        {
          type: 'dropdown',
          label: 'Documentação',
          position: 'left',
          items: [
            {to: '/docs/metodologia', label: 'Metodologia'},
            {to: '/docs/catalogo-tipos-penais', label: 'Catálogo de tipos penais'},
            {to: '/docs/beneficios-penais', label: 'Benefícios penais'},
            {to: '/docs/dados-abertos', label: 'Dados abertos'},
          ],
        },
        {to: '/docs/roadmap', label: 'Roadmap', position: 'left'},
        {to: '/release-notes', label: 'Release notes', position: 'left'},
        {
          href: 'https://github.com/amorim-rc/sispenas',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Ferramenta',
          items: [
            {label: 'Busca por tipo penal', to: '/pesquisa/tipos'},
            {label: 'Busca por benefício', to: '/pesquisa/beneficios'},
            {label: 'Metodologia', to: '/docs/metodologia'},
            {label: 'Benefícios penais', to: '/docs/beneficios-penais'},
          ],
        },
        {
          title: 'Projeto',
          items: [
            {label: 'Sobre o SISPENAS', to: '/'},
            {label: 'Roadmap', to: '/docs/roadmap'},
            {label: 'Dados abertos', to: '/docs/dados-abertos'},
          ],
        },
        {
          title: 'Mais',
          items: [
            {label: 'GitHub', href: 'https://github.com/amorim-rc/sispenas'},
          ],
        },
      ],
      copyright: `SISPENAS © ${new Date().getFullYear()} — Equipe SISPENAS. Licença MIT com atribuição. Ferramenta de pesquisa; não constitui aconselhamento jurídico.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;

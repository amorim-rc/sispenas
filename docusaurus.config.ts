import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'SISPENAS',
  tagline: 'Sistema de Pesquisa de Tipos Penais e Benefícios — Brasil',
  favicon: 'img/favicon.ico',

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
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/sispenas-social-card.jpg',
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
        {to: '/', label: 'Pesquisa', position: 'left', activeBasePath: '/'},
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Documentação',
        },
        {to: '/docs/roadmap', label: 'Roadmap', position: 'left'},
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
            {label: 'Pesquisa de tipos penais', to: '/'},
            {label: 'Metodologia', to: '/docs/metodologia'},
            {label: 'Benefícios penais', to: '/docs/beneficios-penais'},
          ],
        },
        {
          title: 'Projeto',
          items: [
            {label: 'Sobre', to: '/docs/sobre'},
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

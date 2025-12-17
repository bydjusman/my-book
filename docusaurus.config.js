// @ts-check
// `@type` JSDoc annotations allow IDEs and type-checking tools to autocomplete and validate
// You can also use the `@docusaurus/module-type-aliases` package to import the types

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A Comprehensive Guide to Embodied Intelligence',
  favicon: 'img/logo.png',

  // Set the production url of your site here
  url: 'https://my-book-smoky-alpha.vercel.app',
  baseUrl: '/', // Changed from '/my-book/' for root domain deployment

  // Deployment config - can be removed if not deploying to GitHub Pages
  organizationName: 'bydjusman',
  projectName: 'my-book',

  // Broken links handling
  onBrokenLinks: 'throw',

  // Removed deprecated onBrokenMarkdownLinks
  // Added markdown hooks instead:
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn', // ya 'throw' agar chaho ke error ho
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl:
            'https://github.com/bydjusman/my-book/edit/main/',
        },
        blog: false, // Disable blog for textbook
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        logo: {
          alt: 'Robotics Book Logo',
          src: 'img/logo.png',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Textbook',
          },
          {
            href: 'https://github.com/bydjusman/my-book',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Textbook',
            items: [
              {
                label: 'Introduction',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/facebook/docusaurus',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.`,
      },
      prism: {
        theme: require('prism-react-renderer').themes.github,
        darkTheme: require('prism-react-renderer').themes.dracula,
      },
    }),
};

module.exports = config;

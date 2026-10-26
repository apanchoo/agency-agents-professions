const config = {
  title: 'Agency / Professions',
  tagline: 'Open-source AI agents. Specialist thinking. Professional depth.',
  url: 'https://apanchoo.github.io',
  baseUrl: '/agency-agents-professions/',
  organizationName: 'apanchoo',
  projectName: 'agency-agents-professions',
  trailingSlash: true,
  onBrokenLinks: 'throw',
  favicon: 'img/mark.svg',
  i18n: {defaultLocale: 'en', locales: ['en']},
  presets: [['classic', {
    docs: {sidebarPath: require.resolve('./sidebars.js'), routeBasePath: 'docs'},
    blog: false,
    theme: {customCss: require.resolve('./src/css/custom.css')},
  }]],
  themeConfig: {
    image: 'img/social-site.png',
    metadata: [
      {property: 'og:image:width', content: '1200'},
      {property: 'og:image:height', content: '630'},
      {property: 'og:image:alt', content: 'Agency Professions: 2,206 AI agents and 1,923 companion skills, built from France Travail open data.'},
      {name: 'twitter:image:alt', content: 'Open-source professional AI agent library, built from France Travail open data.'},
    ],
    colorMode: {defaultMode: 'light', disableSwitch: true, respectPrefersColorScheme: false},
    navbar: {
      title: 'AGENCY / PROFESSIONS',
      logo: {alt: 'Agency Professions', src: 'img/mark.svg'},
      items: [
        {type: 'custom-iconLink', icon: 'compass', to: '/explorer', label: 'Explore the library', position: 'right'},
        {type: 'custom-iconLink', icon: 'book', to: '/docs/intro', label: 'Documentation', position: 'right'},
        {type: 'custom-iconLink', icon: 'github', href: 'https://github.com/apanchoo/agency-agents-professions', label: 'GitHub', position: 'right'},
      ],
    },
    footer: {style: 'dark', copyright: `Agency Agents + Professional Library · MIT and source-specific licenses · ${new Date().getFullYear()}`},
  },
  headTags: [
    {tagName: 'meta', attributes: {name: 'referrer', content: 'strict-origin-when-cross-origin'}},
    ...(process.env.NODE_ENV === 'production' ? [{tagName: 'meta', attributes: {'http-equiv': 'Content-Security-Policy', content: "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'"}}] : []),
  ],
};
module.exports = config;

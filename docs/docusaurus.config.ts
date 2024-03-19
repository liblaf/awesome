import type * as Preset from "@docusaurus/preset-classic";
import type { Config } from "@docusaurus/types";
import type * as SearchLocal from "@easyops-cn/docusaurus-search-local";

const config: Config = {
  title: "Awesome",
  url: "https://awesome.liblaf.me",
  baseUrl: "/",
  favicon:
    "https://api.iconify.design/simple-icons/awesomelists.svg?color=%2306b6d4",

  themeConfig: {
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: "Awesome",
      logo: {
        src: "https://api.iconify.design/simple-icons/awesomelists.svg?color=%2306b6d4",
      },
      items: [
        {
          label: "GitHub",
          href: "https://github.com/liblaf/awesome",
          position: "right",
        },
      ],
    },
    docs: {
      sidebar: {
        hideable: true,
      },
    },
  } satisfies Preset.ThemeConfig,

  themes: [
    [
      "@easyops-cn/docusaurus-search-local",
      {
        indexDocs: true,
        indexBlog: false,
        indexPages: false,
        docsRouteBasePath: "/",
        language: ["en", "zh"],
        hashed: true,
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
      } satisfies SearchLocal.PluginOptions,
    ],
  ],

  presets: [
    [
      "classic",
      {
        docs: {
          editUrl: "https://github.com/liblaf/awesome/tree/main/docs/",
          routeBasePath: "/",
          showLastUpdateAuthor: true,
          showLastUpdateTime: true,
        },
        blog: false,
        pages: false,
      } satisfies Preset.Options,
    ],
  ],
};

export default config;

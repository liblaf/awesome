import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

const TITLE: string = "Awesome";
const FAVICON: string =
  "https://api.iconify.design/simple-icons/awesomelists.svg?color=%2306b6d4";

const config: Config = {
  title: TITLE,
  url: "https://awesome.liblaf.me",
  baseUrl: "/",

  favicon: FAVICON,
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  themeConfig: {
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: TITLE,
      logo: {
        src: FAVICON,
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

  themes: [],

  presets: [
    [
      "classic",
      {
        docs: {
          routeBasePath: "/",
          sidebarPath: "./sidebars.ts",
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

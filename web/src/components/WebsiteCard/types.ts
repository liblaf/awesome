export type Website = {
  description?: string;
  favicon: string;
  image?: string;
  title?: string;
  url: string;
};

export const DEMO_WEBSITE: Website = {
  description: "DESCRIPTION",
  favicon: "https://icons.bitwarden.net/example.com/icon.png",
  title: "TITLE",
  url: "https://example.com",
};

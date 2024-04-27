export type Repo = {
  forkCount: number;
  name: string;
  nameWithOwner: string;
  owner: string;
  primaryLanguage?: Language;
  shortDescriptionHTML: string;
  stargazerCount: number;
  url: string;
};

export type Language = {
  color: string;
  name: string;
};

export const DEMO_REPO: Repo = {
  forkCount: 0,
  name: "NAME",
  nameWithOwner: "OWNER/NAME",
  owner: "OWNER",
  primaryLanguage: {
    color: "#000000",
    name: "LANGUAGE",
  },
  shortDescriptionHTML: "🔴 DESCRIPTION",
  stargazerCount: 0,
  url: "https://github.com/OWNER/NAME",
};

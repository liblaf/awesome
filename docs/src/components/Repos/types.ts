export type Repo = {
  description: string;
  full_name: string;
  html_url: string;
  name: string;
  stargazers_count: number;
};

export type Collection = {
  repos: Repo[];
};

export type Data = {
  data: Record<string, Collection>;
};

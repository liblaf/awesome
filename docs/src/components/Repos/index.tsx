import DATA from "@site/data/github.json";
import RepoComponent from "./Repo";
import type { Collection, Repo } from "./types";

export default function Repos({ name }: { name: string }): JSX.Element {
  const data: Collection = DATA.data[name] ?? {
    repos: [
      {
        description: "Awesome Lists",
        full_name: "liblaf/awesome",
        html_url: "https://github.com/liblaf/awesome",
        name: "awesome",
        stargazers_count: 1,
      },
    ],
    websites: [
      {
        url: "https://github.com/",
        title: "GitHub: Let’s build from here · GitHub",
        image:
          "https://github.githubassets.com/assets/campaign-social-031d6161fa10.png",
        description:
          "GitHub is where over 100 million developers shape the future of software, together. Contribute to the open source community, manage your Git repositories, review code like a pro, track bugs and fea...",
        favicon: "https://icons.bitwarden.net/github.com/icon.png",
      },
    ],
  };
  return (
    <ul>
      {data.repos.map((repo: Repo) => (
        <li>
          <RepoComponent repo={repo} />
        </li>
      ))}
    </ul>
  );
}

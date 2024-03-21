import DATA from "@site/data/awesome.json";
import type { Repo } from "@site/src/components/RepoCard";
import RepoCard from "@site/src/components/RepoCard";
import styles from "./styles.module.css";
import type { Website } from "@site/src/components/WebsiteCard";
import WebsiteCard from "@site/src/components/WebsiteCard";

type Data = {
  repos: Repo[];
  websites: Website[];
};

const DEMO: Data = {
  repos: [
    {
      description: "Awesome Lists",
      forks: 0,
      full_name: "liblaf/awesome",
      html_url: "https://github.com/liblaf/awesome",
      language: "Python",
      name: "awesome",
      owner: "liblaf",
      stars: 1,
    },
  ],
  websites: [
    {
      description:
        "GitHub is where over 100 million developers shape the future of software, together. Contribute to the open source community, manage your Git repositories, review code like a pro, track bugs and fea...",
      favicon: "https://icons.bitwarden.net/github.com/icon.png",
      image:
        "https://github.githubassets.com/assets/campaign-social-031d6161fa10.png",
      title: "GitHub: Let’s build from here · GitHub",
      url: "https://github.com/",
    },
  ],
};

export default function AwesomeList({ name }: { name?: string }): JSX.Element {
  const data: Data = DATA.data[name] ?? DEMO;
  return (
    <div className={styles.cards}>
      {data.websites
        .sort(
          (a: Website, b: Website): number =>
            (a.description?.length ?? 0) - (b.description?.length ?? 0)
        )
        .map(
          (website: Website): JSX.Element => (
            <WebsiteCard website={website} />
          )
        )}
      {data.repos
        .sort((a: Repo, b: Repo): number => b.stars - a.stars)
        .map(
          (repo: Repo): JSX.Element => (
            <RepoCard repo={repo} />
          )
        )}
    </div>
  );
}

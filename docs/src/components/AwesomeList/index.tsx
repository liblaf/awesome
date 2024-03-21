import DATA from "@site/data/awesome.json";
import type { Repo } from "@site/src/components/RepoCard";
import RepoCard from "@site/src/components/RepoCard";
import styles from "./styles.module.css";

type Data = {
  repos: Repo[];
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
};

export default function AwesomeList({ name }: { name?: string }): JSX.Element {
  const data: Data = DATA.data[name] ?? DEMO;
  return (
    <div className={styles.cards}>
      {data.repos.map(
        (repo: Repo): JSX.Element => (
          <RepoCard repo={repo} />
        )
      )}
    </div>
  );
}

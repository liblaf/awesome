import { DEMO_REPO, Repo } from "@site/src/components/RepoCard/types";
import { Item } from "./types";
import DATA from "@site/data/data.json";
import styles from "./styles.module.css";
import RepoCard from "../RepoCard";

const GITHUB: Record<string, Repo> = DATA.github ?? {};

export default function AwesomeList({ items }: { items: Item[] }): JSX.Element {
  for (const item of items) {
    console.log(JSON.stringify(item));
  }
  const repos: Repo[] = items
    .filter((item) => item.github)
    .map((item) => {
      let repo: Repo | undefined = GITHUB[item.github];
      let [owner, name] = item.github.split("/");
      if (!repo) {
        repo = {
          ...DEMO_REPO,
          name: name,
          nameWithOwner: item.github,
          owner: owner,
          url: `https://github.com/${item.github}`,
        };
      }
      return repo;
    })
    .sort((a, b) => {
      return b.stargazerCount - a.stargazerCount;
    });
  return (
    <div className={styles.cards}>
      {repos.map((repo) => (
        <RepoCard repo={repo} key={repo.url} />
      ))}
    </div>
  );
}

import DATA from "@site/data/data.json";
import { DEMO_REPO, Repo } from "@site/src/components/RepoCard/types";
import RepoCard from "../RepoCard";
import WebsiteCard from "../WebsiteCard";
import { DEMO_WEBSITE, Website } from "../WebsiteCard/types";
import styles from "./styles.module.css";
import { Item } from "./types";

const GITHUB: Record<string, Repo> = DATA.github ?? {};
const WEBSITE: Record<string, Website> = DATA.website ?? {};

export default function AwesomeList({ items }: { items: Item[] }): JSX.Element {
  for (const item of items) {
    console.log(JSON.stringify(item));
  }
  const websites: Website[] = items
    .filter((item) => item.website)
    .map((item) => {
      let website: Website | undefined = WEBSITE[item.website];
      if (!website) {
        website = {
          ...DEMO_WEBSITE,
          title: item.website,
          url: item.website,
        };
      }
      return website;
    });
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
      {websites.map((website) => (
        <WebsiteCard website={website} key={website.url} />
      ))}
      {repos.map((repo) => (
        <RepoCard repo={repo} key={repo.url} />
      ))}
    </div>
  );
}

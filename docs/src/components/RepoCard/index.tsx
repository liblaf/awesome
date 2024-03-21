import Link from "@docusaurus/Link";
import { Icon } from "@iconify/react";
import clsx from "clsx";
import Description from "./Description";
import Language from "./Language";
import Meta from "./Meta";
import styles from "./styles.module.css";

export type Repo = {
  activity_score: number;
  description?: string;
  forks: number;
  full_name: string;
  html_url: string;
  language?: string;
  name: string;
  owner: string;
  stars: number;
};

function prettyNumber(num: number): string {
  return num
    .toLocaleString(undefined, {
      maximumSignificantDigits: 3,
      notation: "compact",
    })
    .toLowerCase();
}

export default function RepoCard({ repo }: { repo: Repo }): JSX.Element {
  return (
    <Link
      className={clsx("card", styles.card)}
      title={repo.full_name}
      to={repo.html_url}
    >
      <div className={styles.title}>
        <Icon className={styles.icon} icon="octicon:repo-16" />
        {repo.full_name.length < 31 ? (
          <span className={styles.owner}>{repo.owner}/</span>
        ) : (
          <></>
        )}
        <span className={styles.name}>{repo.name}</span>
      </div>
      <Description>{repo.description}</Description>
      <p className={styles.meta}>
        <Language language={repo.language} />
        <Meta icon="octicon:star-16">{prettyNumber(repo.stars)}</Meta>
        <Meta icon="octicon:repo-forked-16">{prettyNumber(repo.forks)}</Meta>
        <Meta icon="octicon:flame-16">{prettyNumber(repo.activity_score)}</Meta>
      </p>
    </Link>
  );
}

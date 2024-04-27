import Link from "@docusaurus/Link";
import clsx from "clsx";
import Description from "./Description";
import Language from "./Language";
import Meta from "./Meta";
import Title from "./Title";
import styles from "./styles.module.css";
import { DEMO_REPO, Repo } from "./types";

export default function RepoCard({ repo }: { repo?: Repo }): JSX.Element {
  if (!repo) {
    repo = DEMO_REPO;
  }
  return (
    <Link
      className={clsx("card", styles.card)}
      title={repo.nameWithOwner}
      to={repo.url}
    >
      <Title name={repo.name} />
      <Description html={repo.shortDescriptionHTML} />
      <div className={styles.meta}>
        <Language language={repo.primaryLanguage} />
        <Meta icon="octicon:star-16" data={repo.stargazerCount} />
        <Meta icon="octicon:repo-forked-16" data={repo.forkCount} />
      </div>
    </Link>
  );
}

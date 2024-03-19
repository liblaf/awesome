import Link from "@docusaurus/Link";
import { Icon } from "@iconify/react";
import styles from "./styles.module.css";
import type { Repo } from "./types";

function Stars({ stars }: { stars: number }): JSX.Element {
  return (
    <>
      <Icon className={styles.icon} icon="octicon:star-fill-16" />
      {stars.toLocaleString()}
    </>
  );
}

export default function Repo({ repo }: { repo: Repo }): JSX.Element {
  return (
    <>
      <Link title={repo.full_name} to={repo.html_url}>
        {repo.name}
      </Link>
      {" ( "}
      <Stars stars={repo.stargazers_count} />
      {" )"}
      {repo.description ? <> &mdash; {repo.description} </> : null}
    </>
  );
}

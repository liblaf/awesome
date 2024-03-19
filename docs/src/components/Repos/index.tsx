import DATA from "@site/data/github.json";
import RepoComponent from "./Repo";
import type { Collection, Repo } from "./types";

export default function Repos({ name }: { name: string }): JSX.Element {
  const data: Collection = DATA.data[name] ?? DATA.data["Hello"];
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

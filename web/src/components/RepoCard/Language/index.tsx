import type { Language as Lang } from "../types";
import styles from "./styles.module.css";

export default function Language({
  language,
}: {
  language?: Lang;
}): JSX.Element {
  if (!language) {
    return <></>;
  }
  return (
    <span className={styles.language}>
      <span
        className={styles.languageColor}
        style={{ backgroundColor: language.color }}
      ></span>
      <span>{language.name}</span>
    </span>
  );
}

import styles from "./styles.module.css";

export default function Language({
  language,
}: {
  language?: string;
}): JSX.Element {
  if (!language) {
    return <></>;
  }
  return (
    <span className={styles.language}>
      <span
        className={styles["language-color"]}
        style={{ backgroundColor: "TODO" }}
      ></span>
      <span>{language}</span>
    </span>
  );
}

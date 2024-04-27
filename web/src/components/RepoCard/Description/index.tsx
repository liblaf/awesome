import styles from "./styles.module.css";

export default function Description({ html }: { html?: string }): JSX.Element {
  return (
    <div
      className={styles.description}
      dangerouslySetInnerHTML={{ __html: html }}
    ></div>
  );
}

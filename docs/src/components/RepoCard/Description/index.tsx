import styles from "./styles.module.css";

export default function Description({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element {
  return <p className={styles.description}>{children}</p>;
}

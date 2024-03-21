import styles from "./styles.module.css";

export default function Description({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element {
  if (!children) {
    return <></>;
  }
  return <p className={styles.description}>{children}</p>;
}

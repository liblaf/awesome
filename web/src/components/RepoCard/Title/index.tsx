import { Icon } from "@iconify/react";
import styles from "./styles.module.css";

export default function Title({ name }: { name: string }): JSX.Element {
  return (
    <div className={styles.title}>
      <Icon className={styles.icon} icon="octicon:repo-16" />
      <span className={styles.name}>{name}</span>
    </div>
  );
}

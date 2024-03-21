import { Icon } from "@iconify/react";
import styles from "./styles.module.css";

export default function Meta({
  icon,
  children,
}: {
  icon: string;
  children: React.ReactNode;
}): JSX.Element {
  if (!children) {
    return <></>;
  }
  return (
    <span className={styles.meta}>
      <Icon className={styles.icon} icon={icon} />
      {children}
    </span>
  );
}

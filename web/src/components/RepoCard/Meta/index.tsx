import { Icon } from "@iconify/react";
import styles from "./styles.module.css";

function prettyNumber(num?: number): string | undefined {
  return num
    ?.toLocaleString(undefined, {
      maximumSignificantDigits: 3,
      notation: "compact",
    })
    .toLowerCase();
}

export default function Meta({
  icon,
  data,
}: {
  icon: string;
  data?: number;
}): JSX.Element {
  if (data === undefined) {
    return <></>;
  }
  return (
    <span className={styles.meta}>
      <Icon className={styles.icon} icon={icon} />
      {prettyNumber(data)}
    </span>
  );
}

import { Icon } from "@iconify/react";
import clsx from "clsx";
import { ICONS } from "./constants";
import styles from "./styles.module.css";

export default function Badage({ name }: { name: string }): JSX.Element {
  return (
    <span className={clsx(styles.badage, styles[name])}>
      <Icon icon={ICONS[name]} />
      <span> {name} </span>
    </span>
  );
}

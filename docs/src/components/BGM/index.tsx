import Link from "@docusaurus/Link";
import { Icon } from "@iconify/react";
import DATA from "@site/data/bgm.json";
import clsx from "clsx";
import { ICONS, TYPES } from "./constants";
import styles from "./styles.module.css";

type Collection = {
  subject_id: number;
  rate: number;
  type: number;
  subject: {
    id: number;
    name: string;
    name_cn: string;
    date: string;
    images: {
      large: string;
      common: string;
      medium: string;
      small: string;
      grid: string;
    };
    score: number;
  };
};

export default function BGM({ rate }: { rate: number }): JSX.Element {
  const data = DATA.data as Collection[];
  const collections: Collection[] = data.filter(
    (collection: Collection): boolean => collection.rate === rate
  );
  return (
    <div className={styles.cards}>
      {collections.map((collection: Collection): JSX.Element => {
        const name: string =
          collection.subject.name_cn || collection.subject.name;
        const type_name: string = TYPES[collection.type];
        const type_style: string = styles[type_name];
        return (
          <Link
            className={clsx(styles.card, type_style)}
            key={collection.subject_id}
            href={`https://bgm.tv/subject/${collection.subject.id}`}
          >
            <figure className={styles.figure}>
              <img alt={name} src={collection.subject.images.large} />
              <figcaption className={styles.name}>
                <Icon icon={ICONS[type_name]} />
                <span> {name} </span>
              </figcaption>
              <div className={styles.info}>
                {collection.subject.date}
                {" / "}
                {collection.subject.score}
              </div>
            </figure>
          </Link>
        );
      })}
    </div>
  );
}

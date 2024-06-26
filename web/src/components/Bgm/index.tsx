import Link from "@docusaurus/Link";
import DATA from "@site/data/bgm.json";
import Badge from "./Badge";
import { TYPES } from "./constants";
import styles from "./styles.module.css";
import { Image } from "@arco-design/web-react";
import { Icon } from "@iconify/react/dist/iconify.js";

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

export default function Bgm({ rate }: { rate: number }): JSX.Element {
  const data = DATA.data as Collection[];
  const collections_unordered: Collection[] = data.filter(
    (collection: Collection): boolean => collection.rate === rate,
  );
  const collections: Collection[] = collections_unordered.sort(
    (a: Collection, b: Collection): number => {
      const a_date = new Date(a.subject.date);
      const b_date = new Date(b.subject.date);
      return b_date.getTime() - a_date.getTime();
    },
  );
  return (
    <div className={styles.cards}>
      {collections.map((collection: Collection): JSX.Element => {
        const name: string =
          collection.subject.name_cn || collection.subject.name;
        const type_name: string = TYPES[collection.type];
        return (
          <Link
            className={styles.card}
            key={collection.subject_id}
            title={name}
            to={`https://bgm.tv/subject/${collection.subject.id}`}
          >
            <figure>
              <div className={styles.cover}>
                <Badge name={type_name} />
                <Image alt={name} src={collection.subject.images.large} />
              </div>
              <figcaption className={styles.title}>
                <div> {name} </div>
              </figcaption>
              <div className={styles.info}>
                <Icon className={styles.star} icon="octicon:star-fill-16" />
                {collection.subject.score.toFixed(1)}
                {" / "}
                {collection.subject.date}
              </div>
            </figure>
          </Link>
        );
      })}
    </div>
  );
}

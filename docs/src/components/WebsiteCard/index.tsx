import Link from "@docusaurus/Link";
import clsx from "clsx";
import styles from "./styles.module.css";
import Description from "./Description";

export type Website = {
  description?: string;
  favicon: string;
  image?: string;
  title?: string;
  url: string;
};

function Favicon({ src }: { src?: string }): JSX.Element {
  if (!src) {
    return <></>;
  }
  return <img className={styles.favicon} src={src} />;
}

export default function WebsiteCard({
  website,
}: {
  website: Website;
}): JSX.Element {
  let background: React.CSSProperties = undefined;
  if (website.image) {
    background = {
      background: `url(${website.image}) center center / cover no-repeat`,
    };
  }
  return (
    <Link
      className={clsx(
        "card",
        styles.card,
        website.image ? styles.image : undefined,
      )}
      style={background}
      to={website.url}
    >
      <div className={styles.detail}>
        <div className={styles.title}>
          <Favicon src={website.favicon} />
          <span>{website.title ?? website.url}</span>
        </div>
        <Description>{website.description}</Description>
      </div>
    </Link>
  );
}

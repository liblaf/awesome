import Link from "@docusaurus/Link";
import clsx from "clsx";
import Description from "./Description";
import styles from "./styles.module.css";
import { Website } from "./types";

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
  const title: string = website.title ?? website.url;
  return (
    <Link
      className={clsx(
        "card",
        styles.card,
        website.image ? styles.image : undefined,
      )}
      style={background}
      title={title}
      to={website.url}
    >
      <div className={styles.detail}>
        <div className={styles.title}>
          <Favicon src={website.favicon} />
          <span>{title}</span>
        </div>
        <Description>{website.description}</Description>
      </div>
    </Link>
  );
}

import Markdown from "react-markdown";
import remarkGemoji from "remark-gemoji";
import remarkGfm from "remark-gfm";
import styles from "./styles.module.css";

export default function Description({
  children,
}: {
  children?: string;
}): JSX.Element {
  return (
    <Markdown
      className={styles.description}
      remarkPlugins={[remarkGemoji, remarkGfm]}
    >
      {children}
    </Markdown>
  );
}

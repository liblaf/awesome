import getTitleAtUrl from "get-title-at-url";

interface Website {
  favicon?: string;
  title?: string;
  url: string;
}

export async function websites(
  groups: Record<string, Website[]>,
): Promise<Record<string, Website[]>> {
  for (const group in groups) {
    groups[group] = await Promise.all(
      groups[group].map(async (website: Website): Promise<Website> => {
        if (!website.title) {
          website.title = website.url;
          try {
            const { title }: { title: string } = await getTitleAtUrl(
              website.url,
            );
            if (title) {
              website.title = title;
            }
          } catch (error) {
            console.error(error);
          }
        }
        const url = new URL(website.url);
        website.favicon = `https://melodic-scarlet-wolverine.faviconkit.com/${url.hostname}/256`;
        return website;
      }),
    );
  }
  return groups;
}

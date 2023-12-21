interface Repo {
  commits: number;
  description: string;
  name: string;
  stars: number;
  url: string;
}

async function retry<T>(
  fn: () => Promise<T>,
  maxRetry: number = 3,
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    console.error(error);
    if (maxRetry > 0) {
      return await retry(fn, maxRetry - 1);
    } else {
      throw error;
    }
  }
}

async function fetchWithToken(
  url: string,
  maxRetry: number = 3,
): Promise<Response> {
  return await retry(async (): Promise<Response> => {
    let response: Response = await fetch(url, {
      headers: {
        ...(process.env.GH_TOKEN
          ? { Authorization: `Bearer ${process.env.GH_TOKEN}` }
          : {}),
      },
    });
    if (response.ok) {
      return response;
    } else {
      throw new Error(
        `failed to fetch ${url}: ${response.status} ${response.statusText}`,
      );
    }
  }, maxRetry);
}

export async function github(
  groups: Record<string, string[]>,
): Promise<Record<string, Repo[]>> {
  const results: Record<string, Repo[]> = {};
  for (const group in groups) {
    const repos: Repo[] = await Promise.all(
      groups[group].map(async (repo): Promise<Repo> => {
        try {
          const data: {
            description: string;
            name: string;
            stargazers_count: number;
            html_url: string;
          } = await retry(
            async (): Promise<{
              description: string;
              name: string;
              stargazers_count: number;
              html_url: string;
            }> => {
              const response: Response = await fetchWithToken(
                `https://api.github.com/repos/${repo}`,
              );
              return await response.json();
            },
          );
          let commits: number = NaN;
          try {
            commits = await retry(async (): Promise<number> => {
              const commitActivityResponse: Response = await fetchWithToken(
                `https://api.github.com/repos/${repo}/stats/commit_activity`,
              );
              const commitActivity: { total: number }[] =
                await commitActivityResponse.json();
              return commitActivity.reduce(
                (value: number, activity: { total: number }): number => {
                  return value + activity.total;
                },
                0,
              );
            });
          } catch (error) {
            console.error(error);
          }
          return {
            commits: commits,
            description: data.description,
            name: data.name,
            stars: data.stargazers_count,
            url: data.html_url,
          };
        } catch (error) {
          console.error(error);
          return {
            commits: NaN,
            description: `${error}`,
            name: repo.split("/")[1],
            stars: NaN,
            url: `https://github.com/${repo}`,
          };
        }
      }),
    );
    results[group] = repos.sort(
      (a: Repo, b: Repo): number => b.stars - a.stars,
    );
  }
  return results;
}

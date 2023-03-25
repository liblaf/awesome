import typing

import github
import github.Repository


def sort_repositories(
    repositories: list, token: typing.Optional[str]
) -> list[github.Repository.Repository]:
    g = github.Github(token)
    repos: list[github.Repository.Repository] = [g.get_repo(r) for r in repositories]
    repos = sorted(repos, key=lambda r: r.stargazers_count, reverse=True)
    return repos

import enum
from typing import Callable

from .github import Client, Commit


class Strategy(str, enum.Enum):
    NO_SKIP = "no-skip"
    NO_SKIP_MIGRATIONS = "no-skip-migrations"


def no_skip(client: Client, commits: list[Commit]) -> Commit:
    return commits[0]


def no_skip_migrations(client: Client, commits: list[Commit]) -> Commit:
    """
    Allow a migration to be skipped, unless it contains migrations.
    """

    raise NotImplementedError


STRATEGIES: dict[Strategy, Callable[[Client, list[Commit]], Commit]] = {
    Strategy.NO_SKIP: no_skip,
    Strategy.NO_SKIP_MIGRATIONS: no_skip_migrations,
}


def choose_commit_to_deploy(
    *, client: Client, strategy: Strategy, commits: list[Commit]
) -> Commit:
    return STRATEGIES[strategy](client, commits)

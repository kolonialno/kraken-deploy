import argparse

import pydantic

from .conditions import Condition
from .deploy import maybe_deploy_next
from .github import GithubClient
from .settings import Settings


class EnvironmentConfig(pydantic.BaseModel):
    name: str
    conditions: list[Condition]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--branch",
        type=str,
        help=(
            "Branch to deploy from. If not specified or "
            "empty the project's default branch is used"
        ),
    )
    parser.add_argument(
        "environments",
        type=str,
        help="JSON containing configuration for each environments",
    )

    args = parser.parse_args()

    settings = Settings()
    client = GithubClient(
        repo=settings.GITHUB_REPOSITORY,
        base_url=settings.GITHUB_API_URL,
        token=settings.GITHUB_TOKEN,
    )

    environments = pydantic.parse_raw_as(list[EnvironmentConfig], args.environments)
    for environment in environments:
        print(f"Checking {environment.name}")
        maybe_deploy_next(
            client=client,
            environment=environment.name,
            conditions=environment.conditions,
            branch=args.branch if args.branch else None,
        )


if __name__ == "__main__":
    main()

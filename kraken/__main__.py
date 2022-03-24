from .deploy import maybe_deploy_next
from .github import GithubClient
from .settings import Settings
from .strategies import Strategy


def main() -> None:
    settings = Settings()
    client = GithubClient(
        repo=settings.GITHUB_REPOSITORY,
        base_url=settings.GITHUB_API_URL,
        token=settings.GITHUB_TOKEN,
    )
    maybe_deploy_next(
        client=client, environment="prod", rollout_strategy=Strategy.NO_SKIP
    )


if __name__ == "__main__":
    main()

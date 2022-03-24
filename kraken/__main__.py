from .deploy import maybe_deploy_next
from .github import GithubClient
from .settings import Settings


def main() -> None:
    settings = Settings()
    client = GithubClient(
        repo=settings.GITHUB_REPOSITORY,
        base_url=settings.GITHUB_API_URL,
        token=settings.GITHUB_TOKEN,
    )
    maybe_deploy_next(
        client=client,
        environment="prod",
        # TODO: Find a way to provide rules as input
        rules=[],
    )


if __name__ == "__main__":
    main()

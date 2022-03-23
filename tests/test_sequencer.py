from typing import Callable

from kraken.deploy import maybe_deploy_next
from kraken.github import Client, Commit
from kraken.strategies import Strategy


def test_first_deploy(client: Client, make_commit: Callable[..., Commit]) -> None:
    make_commit(sha="foo")
    commit_2 = make_commit(sha="bar")

    maybe_deploy_next(
        client=client, environment="prod", rollout_strategy=Strategy.NO_SKIP
    )

    deploy = client.get_latest_deployment(environment="prod")
    assert deploy
    assert deploy.sha == commit_2.sha  # Should deploy latest commit

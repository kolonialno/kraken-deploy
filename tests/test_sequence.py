from typing import Callable

from kraken.deploy import maybe_deploy_next
from kraken.github import Client, Commit


def test_first_deploy(client: Client, make_commit: Callable[..., Commit]) -> None:
    make_commit(sha="foo")
    commit_2 = make_commit(sha="bar")

    deployed_commit = maybe_deploy_next(
        client=client, environment="prod", conditions=[]
    )
    assert deployed_commit == commit_2

    deploy = client.get_latest_deployment(environment="prod")
    assert deploy
    assert deploy.sha == commit_2.sha  # Should deploy latest commit


def test_nothing_more_to_deploy(
    client: Client,
    make_commit: Callable[..., Commit],
    make_successful_deployment: Callable[..., None],
) -> None:

    commit = make_commit(sha="foo")
    make_successful_deployment(environment="prod", commit=commit.sha)

    deployed_commit = maybe_deploy_next(
        client=client, environment="prod", conditions=[]
    )
    assert not deployed_commit


def test_deploy_next_commit(
    client: Client,
    make_commit: Callable[..., Commit],
    make_successful_deployment: Callable[..., None],
) -> None:

    commit_1 = make_commit(sha="foo")
    commit_2 = make_commit(sha="bar")
    make_successful_deployment(environment="prod", commit=commit_1.sha)

    deployed_commit = maybe_deploy_next(
        client=client, environment="prod", conditions=[]
    )
    assert deployed_commit == commit_2

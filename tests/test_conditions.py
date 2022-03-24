from typing import Callable

from kraken.conditions import RequiredCheckRun, RequiredDeploy
from kraken.deploy import maybe_deploy_next
from kraken.github import CheckRunConclusion, Client, Commit


def test_missing_check_run(client: Client, commit: Commit) -> None:
    deployed_commit = maybe_deploy_next(
        client=client,
        environment="prod",
        conditions=[
            RequiredCheckRun(type="check-run", name="pytest"),
        ],
    )

    assert deployed_commit is None


def test_successful_check_run(
    client: Client, commit: Commit, make_check_run: Callable[..., None]
) -> None:
    make_check_run(ref=commit.sha, name="pytest")

    deployed_commit = maybe_deploy_next(
        client=client,
        environment="prod",
        conditions=[
            RequiredCheckRun(type="check-run", name="pytest"),
        ],
    )

    assert deployed_commit == commit


def test_failed_check_run(
    client: Client, commit: Commit, make_check_run: Callable[..., None]
) -> None:
    make_check_run(ref=commit.sha, name="pytest", conclusion=CheckRunConclusion.FAILURE)

    deployed_commit = maybe_deploy_next(
        client=client,
        environment="prod",
        conditions=[
            RequiredCheckRun(type="check-run", name="pytest"),
        ],
    )

    assert deployed_commit is None


def test_missing_required_deployment(client: Client, commit: Commit) -> None:
    deployed_commit = maybe_deploy_next(
        client=client,
        environment="prod",
        conditions=[
            RequiredDeploy(type="deploy", environment="staging"),
        ],
    )

    assert deployed_commit is None


def test_required_deployment(
    client: Client, commit: Commit, make_successful_deployment: Callable[..., None]
) -> None:

    make_successful_deployment(environment="staging", commit=commit.sha)

    deployed_commit = maybe_deploy_next(
        client=client,
        environment="prod",
        conditions=[
            RequiredDeploy(type="deploy", environment="staging"),
        ],
    )

    assert deployed_commit == commit

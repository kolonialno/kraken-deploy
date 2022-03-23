from typing import Any, Callable

from kraken.github import Client, Commit


def test_commit(client: Client, commit: Commit) -> None:
    assert commit is not None
    assert commit in client.get_commits(branch="main")


def test_make_commit(client: Client, make_commit: Callable) -> None:
    assert client.get_commits(branch="main", page=1) == []
    commit1 = make_commit(sha="foo")
    assert client.get_commits(branch="main", page=1) == [commit1]
    assert client.get_commits(branch="main", page=2) == []

    commit2 = make_commit(sha="bar")
    assert commit1 != commit2
    assert client.get_commits(branch="main", page=1) == [commit2]
    assert client.get_commits(branch="main", page=2) == [commit1]


def test_successful_deploy(
    client: Client,
    commit: Commit,
    start_deploy: Callable[..., Any],
    finish_deploy: Callable[..., Any],
) -> None:
    deployment = client.get_latest_deployment(environment="prod")
    assert not deployment

    client.create_deployment(environment="prod", commit=commit.sha)

    deployment = client.get_latest_deployment(environment="prod")
    assert deployment
    assert deployment.sha == commit.sha
    assert deployment.statuses == []
    assert not deployment.is_done

    start_status = start_deploy(environment="prod")

    deployment = client.get_latest_deployment(environment="prod")
    assert deployment
    assert deployment.sha == commit.sha
    assert deployment.statuses == [start_status]
    assert not deployment.is_done

    finish_status = finish_deploy(environment="prod")

    deployment = client.get_latest_deployment(environment="prod")
    assert deployment
    assert deployment.sha == commit.sha
    assert deployment.statuses == [finish_status, start_status]
    assert deployment.is_done


def test_failed_deploy(
    client: Client,
    commit: Commit,
    start_deploy: Callable[..., Any],
    fail_deploy: Callable[..., Any],
) -> None:
    deployment = client.get_latest_deployment(environment="prod")
    assert not deployment

    client.create_deployment(environment="prod", commit=commit.sha)

    deployment = client.get_latest_deployment(environment="prod")
    assert deployment
    assert deployment.sha == commit.sha
    assert deployment.statuses == []
    assert not deployment.is_done

    start_status = start_deploy(environment="prod")

    deployment = client.get_latest_deployment(environment="prod")
    assert deployment
    assert deployment.sha == commit.sha
    assert deployment.statuses == [start_status]
    assert not deployment.is_done

    fail_status = fail_deploy(environment="prod")

    deployment = client.get_latest_deployment(environment="prod")
    assert deployment
    assert deployment.sha == commit.sha
    assert deployment.statuses == [fail_status, start_status]
    assert not deployment.is_done

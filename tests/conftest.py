from datetime import datetime, timezone
from typing import Callable

import pytest

from kraken.github import Commit, Deployment
from kraken.github.types import DeploymentState, DeploymentStatus


class MockClient:
    def __init__(self) -> None:
        self.commits: list[Commit] = []
        self.deployments: dict[str, Deployment] = {}

    def get_latest_deployment(self, *, environment: str) -> Deployment | None:
        return self.deployments.get(environment, None)

    def get_commits(self, *, branch: str, page: int = 1) -> list[Commit]:
        assert page > 0
        assert branch == "main"
        limit = 1
        offset = (page - 1) * limit

        return self.commits[offset : offset + limit]

    def create_deployment(self, *, environment: str, commit: str) -> None:
        assert any(c.sha == commit for c in self.commits)
        self.deployments[environment] = Deployment(
            sha=commit,
            task="deploy",
            environment=environment,
            description="",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            statuses=[],
        )


@pytest.fixture
def client() -> MockClient:
    return MockClient()


@pytest.fixture
def make_commit(client: MockClient) -> Callable[..., Commit]:
    def inner(*, sha: str) -> Commit:
        assert not any(c.sha == sha for c in client.commits)
        user = {"name": "John Doe", "email": "john@example.com"}
        commit = Commit.parse_obj(
            {
                "sha": sha,
                "html_url": f"https://example.com/commits/{sha}",
                "commit": {
                    "message": "Hello world!",
                    "author": user,
                    "committer": user,
                },
            }
        )
        client.commits.insert(0, commit)
        return commit

    return inner


@pytest.fixture
def commit(make_commit: Callable[..., Commit]) -> Commit:
    return make_commit(sha="foo")


@pytest.fixture
def create_deployment_status(client: MockClient):
    def inner(*, environment: str, state: DeploymentState) -> DeploymentStatus:
        assert environment in client.deployments, "Deployment must exist"
        status = DeploymentStatus(state=state, description="", log_url="")
        deployment = client.deployments[environment]
        deployment.statuses.insert(0, status)
        return status

    return inner


@pytest.fixture
def start_deploy(create_deployment_status: Callable[..., DeploymentStatus]):
    def inner(*, environment: str) -> DeploymentStatus:
        return create_deployment_status(
            environment=environment, state=DeploymentState.IN_PROGRESS
        )

    return inner


@pytest.fixture
def finish_deploy(create_deployment_status: Callable[..., DeploymentStatus]):
    def inner(*, environment: str) -> DeploymentStatus:
        return create_deployment_status(
            environment=environment, state=DeploymentState.SUCCESS
        )

    return inner


@pytest.fixture
def fail_deploy(create_deployment_status: Callable[..., DeploymentStatus]):
    def inner(*, environment: str) -> DeploymentStatus:
        return create_deployment_status(
            environment=environment, state=DeploymentState.FAILURE
        )

    return inner


@pytest.fixture
def make_successful_deployment(
    client: MockClient, finish_deploy: Callable[..., None]
) -> Callable[..., None]:
    def inner(*, environment: str, commit: str) -> None:
        client.create_deployment(environment=environment, commit=commit)
        finish_deploy(environment=environment)

    return inner

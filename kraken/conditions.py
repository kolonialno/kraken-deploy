from typing import Literal

from pydantic import BaseModel

from .github import CheckRunConclusion, Client, Commit


class RequiredCheckRun(BaseModel):
    type: Literal["check-run"]
    name: str

    @property
    def description(self) -> str:
        return f"check-run {self.name}"


class RequiredDeploy(BaseModel):
    type: Literal["deploy"]
    environment: str

    @property
    def description(self) -> str:
        return f"deploy to {self.environment}"


Condition = RequiredCheckRun | RequiredDeploy


def check_check_run(
    *, client: Client, condition: RequiredCheckRun, commit: Commit
) -> bool:

    check_runs = client.get_check_runs(ref=commit.sha)

    return any(
        check_run.name == condition.name
        and check_run.conclusion == CheckRunConclusion.SUCCESS
        for check_run in check_runs
    )


def check_deploy(*, client: Client, condition: RequiredDeploy, commit: Commit) -> bool:

    commits = {commit.sha} | {
        c.sha for c in reversed(client.get_commits_after(ref=commit.sha))
    }

    for sha in commits:
        deployment = client.get_latest_deployment(
            environment=condition.environment, ref=sha
        )
        if deployment and deployment.is_done:
            return True

    return False


def check_condition(*, client: Client, condition: Condition, commit: Commit) -> bool:
    if isinstance(condition, RequiredDeploy):
        result = check_deploy(client=client, condition=condition, commit=commit)
    elif isinstance(condition, RequiredCheckRun):
        result = check_check_run(client=client, condition=condition, commit=commit)
    else:
        raise RuntimeError(f"Unsupported condition: {condition}")

    if not result:
        print(f'Condition "{condition.description}" not satisfied')

    return result


def check_conditions(
    *, client: Client, conditions: list[Condition], commit: Commit
) -> bool:
    return all(
        check_condition(client=client, condition=condition, commit=commit)
        for condition in conditions
    )

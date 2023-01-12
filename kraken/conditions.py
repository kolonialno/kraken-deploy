from typing import Literal

from pydantic import BaseModel

from .github import CheckRunConclusion, Client, Commit


class RequiredCheckRun(BaseModel):
    type: Literal["check-run"]
    name: str

    @property
    def description(self) -> str:
        return f"check-run {self.name}"

    def __call__(self, commit: Commit, client: Client) -> bool:
        check_runs = client.get_check_runs(ref=commit.sha)
        return any(
            check_run.name == self.name
            and check_run.conclusion == CheckRunConclusion.SUCCESS
            for check_run in check_runs
        )


class RequiredDeploy(BaseModel):
    type: Literal["deploy"]
    environment: str

    @property
    def description(self) -> str:
        return f"deploy to {self.environment}"

    def __call__(self, commit: Commit, client: Client) -> bool:
        commits = {commit.sha} | {
            c.sha for c in reversed(client.get_commits_after(ref=commit.sha))
        }
        for sha in commits:
            deployment = client.get_latest_deployment(
                environment=self.environment, ref=sha
            )
            if deployment and deployment.is_done:
                return True

        return False


Condition = RequiredCheckRun | RequiredDeploy


def check_conditions(
    *, client: Client, conditions: list[Condition], commit: Commit
) -> bool:

    return all(condition(client=client, commit=commit) for condition in conditions)

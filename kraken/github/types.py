from datetime import datetime
from enum import Enum

import pydantic


class DeploymentState(str, Enum):
    ERROR = "error"
    FAILURE = "failure"
    INACTIVE = "inactive"
    IN_PROGRESS = "in_progress"
    QUEUED = "queued"
    PENDING = "pending"
    SUCCESS = "success"
    DESTROYED = "destroyed"


class DeploymentStatus(pydantic.BaseModel):
    state: DeploymentState
    description: str
    log_url: str


class Deployment(pydantic.BaseModel):
    sha: str
    task: str
    environment: str
    description: str
    created_at: datetime
    updated_at: datetime
    statuses: list[DeploymentStatus]

    @property
    def is_done(self) -> bool:
        # TODO: Only check latest status? 🤔
        return any(status.state == "success" for status in self.statuses)


class User(pydantic.BaseModel):
    name: str
    email: str


class CommitDetails(pydantic.BaseModel):
    message: str
    author: User
    commiter: User


class Commit(pydantic.BaseModel):
    sha: str
    html_url: str
    commit: CommitDetails

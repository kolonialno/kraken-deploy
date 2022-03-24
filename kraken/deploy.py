from .conditions import Condition, check_conditions
from .github import Client, Commit


def maybe_deploy_next(
    *, client: Client, environment: str, conditions: list[Condition]
) -> Commit | None:

    latest_deployment = client.get_latest_deployment(environment=environment)
    commits = client.get_commits(branch="main")

    if latest_deployment is None:

        # If there's no pre-existing deployments, deploy the newest commit
        commit_to_deploy = commits[0]

    elif not latest_deployment.is_done:

        return None

    else:

        latest_sha = latest_deployment.sha

        undeployed_commits = client.get_commits_after(branch="main", ref=latest_sha)
        if not undeployed_commits:
            return None

        # Always deploy the oldest commit that's not deployed yet. In the
        # future we might want to allow more complex logic here, like skipping
        # a commit if we have a long deploy queue
        commit_to_deploy = undeployed_commits[-1]

    if not check_conditions(
        client=client, commit=commit_to_deploy, conditions=conditions
    ):
        return None

    print(f"Create deployment: {commit_to_deploy}")

    client.create_deployment(environment=environment, commit=commit_to_deploy.sha)

    return commit_to_deploy

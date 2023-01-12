from .conditions import Condition, check_conditions
from .github import Client, Commit


def maybe_deploy_next(
    *,
    client: Client,
    environment: str,
    conditions: list[Condition],
    branch: str | None = None,
) -> Commit | None:

    latest_deployment = client.get_latest_deployment(environment=environment)
    commits = client.get_commits(branch=branch)

    if latest_deployment is None:

        # If there's no pre-existing deployments, deploy the newest commit
        undeployed_commits = [commits[0]]

    elif not latest_deployment.is_done:

        print("Previous deployment is not done yet")
        return None

    else:

        latest_sha = latest_deployment.sha
        undeployed_commits = client.get_commits_after(ref=latest_sha, branch=branch)

    if not undeployed_commits:
        print("All commits have been deployed")
        return None

    for commit_to_deploy in undeployed_commits:
        if check_conditions(
            client=client, commit=commit_to_deploy, conditions=conditions
        ):
            print(f"Create deployment: {commit_to_deploy.sha}")

            client.create_deployment(
                environment=environment, commit=commit_to_deploy.sha
            )
            return commit_to_deploy
        else:
            print(f"Conditions failed, not deploing {commit_to_deploy.sha}")

    print("No undeployed commits satisfied all conditions, not deploying")
    return None

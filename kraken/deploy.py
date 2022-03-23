from .github import Client
from .strategies import Strategy, choose_commit_to_deploy


def maybe_deploy_next(
    *, client: Client, environment: str, rollout_strategy: Strategy
) -> None:

    latest_deployment = client.get_latest_deployment(environment=environment)
    commits = client.get_commits(branch="main")

    if latest_deployment is None:

        commit_to_deploy = commits[0]

    elif not latest_deployment.is_done:

        return

    else:

        # Load commits until we find the last deployed commit
        i = 1
        while not any(commit.sha == latest_deployment.sha for commit in commits):
            commits.extend(client.get_commits(branch="main", page=i))
            i += 1

        commit_to_deploy = choose_commit_to_deploy(
            client=client, strategy=rollout_strategy, commits=commits
        )

    client.create_deployment(environment=environment, commit=commit_to_deploy.sha)

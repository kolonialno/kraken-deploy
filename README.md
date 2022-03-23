<h1 align="center">
  🐙<br>
  Kraken
</h1>

<p align="center">
  A deploy orchestrator, deploying commits in the correct order.
</p>


## About

Kraken is a deploy orchestrator that runs as a GitHub actions. It does not have
any state itself and relies entirely on the git history and GitHub deployments
to determine what to deploy next.


## Usage

Kraken is used as a GitHub action. Here is an example workflow:


```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    ...
```

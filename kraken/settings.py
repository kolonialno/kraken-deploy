from pydantic import BaseSettings


class Settings(BaseSettings):
    GITHUB_TOKEN: str
    GITHUB_REPOSITORY: str
    GITHUB_API_URL: str

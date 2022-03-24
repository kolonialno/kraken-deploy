# Container image that runs your code
FROM python:3.10-alpine

RUN pip install poetry==1.1.13

COPY pyproject.toml poetry.toml poetry.lock .

RUN poetry install

COPY kraken .

ENTRYPOINT ["python", "-m", "kraken"]

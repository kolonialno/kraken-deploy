all : black mypy isort flake8 pytest

.PHONY: black
black:
	black --check kraken tests

.PHONY: mypy
mypy:
	mypy kraken tests

.PHONY: isort
isort:
	isort --check-only kraken tests

.PHONY: flake8
flake8:
	flake8 kraken tests


.PHONY: pytest
pytest:
	pytest

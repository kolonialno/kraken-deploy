all : black mypy isort flake8

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

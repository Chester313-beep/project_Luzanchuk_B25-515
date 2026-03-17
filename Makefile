.PHONY: install build lint project

install:
	uv sync

build:
	uv build

lint:
	uv run ruff check .

project:
	uv run python -m src.main

test:
	uv run pytest
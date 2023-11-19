default: test lint

docs: install
	poetry run pdoc shakersynth

test: install
	poetry run pytest --cov=shakersynth --cov-report=html

lint: install
	poetry run flake8
	poetry run mypy .

test-watch: install
	poetry run pytest-watch --beforerun=clear --runner='make'

clean:
	rm -rf build dist

build: install clean
	poetry build

install:
	poetry install

publish: build
	poetry publish

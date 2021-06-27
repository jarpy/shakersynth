default: test lint

docs:
	pdoc shakersynth

test:
	pytest --cov=shakersynth --cov-report=html

lint:
	flake8 --config=setup.cfg
	mypy --config-file=setup.cfg .

test-watch:
	pytest-watch --beforerun=clear --runner='make'

clean:
	rm -rf build dist

package: clean
	python3 setup.py sdist bdist_wheel

install: package
	pip install dist/Shakersynth*.tar.gz

publish: package
	python3 -m twine upload dist/*

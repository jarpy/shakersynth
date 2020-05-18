test:
	pytest --cov=shakersynth --cov-report=html
	flake8 --exclude=venv .
	mypy shakersynth

clean:
	rm -rf build dist

package: clean
	python3 setup.py sdist bdist_wheel

install: package
	pip install dist/Shakersynth*.tar.gz

publish: package
	python3 -m twine upload dist/*

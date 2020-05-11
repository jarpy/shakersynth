test:
	pytest
	flake8 shakersynth shakersynth.py
	mypy shakersynth

package:
	python3 setup.py sdist bdist_wheel

install: package
	pip install dist/Shakersynth*.tar.gz

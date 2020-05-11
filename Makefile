test:
	pytest
	flake8 shakersynth shakersynth.py
	mypy shakersynth

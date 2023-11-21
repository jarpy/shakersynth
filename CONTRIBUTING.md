# Prerequisites

## Python

ShakerSynth is currently developed, tested, and supported on Python 3.9. Make
sure you have Python 3.9.x installed and set as your active version.

> :bulb: If you need to manage multiple Python versions on your system, you may
> want to explore [pyenv] or [pyenv for Windows][pyenv-win].

## Libraries

### Linux

On Linux systems, install the required libraries. If you're using a Debian-based
distribution, this should be sufficient:

```shell
apt-get install \
      build-essential \
      portaudio19-dev \
      libsndfile1-dev \
      libportmidi-dev \
      liblo-dev \
      libgtk-3-dev
```

### Windows

On Windows, no manual library installation is needed.

## Poetry

We use [Poetry] as the build system for ShakerSynth. You need it to work on the
project. Install it via Pip:

```shell
pip install poetry
```

# Running ShakerSynth

* Clone this repository
* `cd shakersynth`
* `poetry install`
* `poetry run shakersynth`

# Typing and code quality

ShakerSynth is written in modern, typed Python. We enthusiastically recommend
that you configure your editor to provide realtime hints from [Mypy] and
[Flake8].

> :bulb: You don't need to install Mypy, Flake8 etc. They are automatically
> installed into your ShakerSynth workspace by Poetry, but you should make sure
> your editor takes advantage of them.

# Testing

You can run the test suite with:

```shell
poetry run pytest
```

[Flake8]: https://flake8.pycqa.org/en/latest/
[Mypy]: https://mypy.readthedocs.io/en/stable/index.html
[Poetry]: https://python-poetry.org/
[pyenv]: https://github.com/pyenv/pyenv
[pyenv-win]: https://github.com/pyenv-win/pyenv-win

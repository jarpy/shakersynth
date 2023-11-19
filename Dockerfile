# This Dockerfile builds an image that can be used as a basic development
# environment for ShakerSynth.

FROM python:3.9-bullseye
WORKDIR /shakersynth
RUN apt-get update
RUN apt-get install -y \
      build-essential \
      portaudio19-dev \
      libsndfile1-dev \
      libportmidi-dev \
      liblo-dev \
      libgtk-3-dev \
      vim
RUN pip install poetry
COPY . /shakersynth/
RUN poetry install

ENTRYPOINT ["/bin/bash"]

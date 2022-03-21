FROM python:3.10
WORKDIR /shakersynth
COPY requirements.txt /shakersynth/
RUN apt-get update && \
    apt-get install -y \
      build-essential \
      portaudio19-dev \
      libsndfile1-dev \
      libportmidi-dev \
      liblo-dev \
      libgtk-3-dev && \
    pip install -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/bin/bash"]

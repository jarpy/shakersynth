import logging
from shakersynth.synth.rotor import RotorSynth
from shakersynth.config import config
from typing import Dict  # noqa: F401

log = logging.getLogger(__name__)
log.setLevel(config.log_level)


class Aircraft():
    def __init__(self):
        self.synths = [RotorSynth()]
        self.is_running = False

    def update(self, telemetry: dict):
        for synth in self.synths:
            synth.update(telemetry)

    def start(self):
        for synth in self.synths:
            log.debug("Starting synth: %s" % type(synth))
            synth.start()
        self.is_running = True

    def stop(self):
        for synth in self.synths:
            log.debug("Stopping synth: %s" % type(synth))
            synth.stop()
        self.is_running = False

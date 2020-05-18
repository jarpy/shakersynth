from shakersynth.synth.rotor import RotorSynth
from typing import Dict  # noqa: F401


class Aircraft():
    def __init__(self):
        self.synths = [RotorSynth()]
        self.is_running = False

    def update(self, telemetry: dict):
        for synth in self.synths:
            synth.update(telemetry)

    def start(self):
        for synth in self.synths:
            synth.start()
        self.is_running = True

    def stop(self):
        for synth in self.synths:
            synth.stop()
        self.is_running = False

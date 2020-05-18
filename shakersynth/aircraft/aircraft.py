from shakersynth.synth.rotor import RotorSynth
from typing import Dict  # noqa: F401


class Aircraft():
    def __init__(self):
        self.data = {}  # type: Dict[str, float]
        self.is_running = False
        self.synths = [RotorSynth()]

    def __getitem__(self, key):
        return self.data[key]

    def update(self, telemetry: dict):
        self.data = telemetry
        for synth in self.synths:
            synth.update(self.data)

    def start(self):
        for synth in self.synths:
            synth.start()
        self.is_running = True

    def stop(self):
        for synth in self.synths:
            synth.stop()
        self.is_running = False

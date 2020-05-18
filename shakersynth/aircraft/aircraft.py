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
        self.data["rotor_rpm"] = self._calculate_rotor_rpm()
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

    def _calculate_rotor_rpm(self):
        module = self.data["module"]
        rpm_percent = self.data["rotor_rpm_percent"]

        if(module == "mi-8"):
            # 95 gauge RPM == 192 real rotor RPM. [1, 2]
            return rpm_percent * 2.02105
        elif(module == "uh-1h"):
            # 90 gauge RPM == 324 real rotor RPM. [3]
            return rpm_percent * 3.6
        else:
            return 0.00000001

# 1. http://koavia.com/eng/product/helicopter/hvostovye_valy.shtml#2
# 2. https://www.pprune.org/rotorheads/221789-mil-8-mtv-mtv-1-info.html
# 3. https://apps.dtic.mil/dtic/tr/fulltext/u2/901787.pdf

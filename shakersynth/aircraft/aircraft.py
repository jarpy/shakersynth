import pyo
from shakersynth.synth.rotor import RotorSynth
from typing import Dict  # noqa: F401


class Aircraft():
    def __init__(self, synth_engine: pyo.Server):
        self.data = {}  # type: Dict[str, float]
        self.synth_engine = synth_engine
        self.rotor_synth = RotorSynth(self.synth_engine)

    def __getitem__(self, key):
        return self.data[key]

    def update(self, telemetry: dict):
        self.data = telemetry
        self.data["rotor_rpm"] = self.get_rotor_rpm()
        self.rotor_synth.update(self.data)

    def get_rotor_rpm(self):
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

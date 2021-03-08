import logging
import pyo
from shakersynth.config import config

log = logging.getLogger(__name__)
log.setLevel(config.log_level)


class RotorSynth():
    def __init__(self):
        self.is_running = False
        self.fader0 = pyo.Fader()
        self.fader1 = pyo.Fader()

        self.lorenz0 = pyo.Lorenz(pitch=0.1)
        self.lorenz0_scaled = pyo.Scale(self.lorenz0, outmin=0.3, outmax=0.9)
        self.lorenz1 = pyo.Lorenz(pitch=0.11)
        self.lorenz1_scaled = pyo.Scale(self.lorenz1, outmin=0.3, outmax=0.9)

        self.osc0 = pyo.LFO(freq=0.0001, sharp=self.lorenz0_scaled, mul=self.fader0)
        self.osc1 = pyo.LFO(freq=0.0001, sharp=self.lorenz1_scaled, mul=self.fader1)

        self.filter0 = pyo.Biquad(self.osc0, freq=200)
        self.filter1 = pyo.Biquad(self.osc1, freq=200)

        self.filter0.out(0)
        self.filter1.out(1)

    def update(self, telemetry: dict):
        """Update synth parameters based on telemetry."""
        rpm = self._calculate_rotor_rpm(telemetry)

        if rpm == 0:
            rpm = 0.00000001

        module = telemetry["module"]

        # Revolutions per second is more useful than RPM.
        revolutions_per_second = rpm / 60.0

        if(module == "mi-8"):
            blade_count = 5
        elif(module == "uh-1h"):
            blade_count = 2
        else:
            raise NotImplementedError

        blades_per_second = revolutions_per_second * blade_count

        self.osc0.setFreq(blades_per_second)
        self.osc1.setFreq(blades_per_second)

    def start(self):
        if self.is_running:
            return
        self.fader0.play()
        self.fader1.play()
        self.is_running = True

    def stop(self):
        if not self.is_running:
            return

        self.fader0.stop()
        self.fader1.stop()
        self.is_running = False

    def _calculate_rotor_rpm(self, telemetry: dict) -> float:
        """Given a telemetry payload, return the true RPM of the rotor."""
        module = telemetry["module"]
        rpm_percent = telemetry["rotor_rpm_percent"]

        if(module == "mi-8"):
            # 95 gauge RPM == 192 real rotor RPM. [1, 2]
            # But 200 gives better results in the sim.
            return float(rpm_percent * (200 / 95))
        elif(module == "uh-1h"):
            # 90 gauge RPM == 324 real rotor RPM. [3]
            return float(rpm_percent * (324 / 90))
        else:
            return 0.00000001

# 1. http://koavia.com/eng/product/helicopter/hvostovye_valy.shtml#2
# 2. https://www.pprune.org/rotorheads/221789-mil-8-mtv-mtv-1-info.html
# 3. https://apps.dtic.mil/dtic/tr/fulltext/u2/901787.pdf

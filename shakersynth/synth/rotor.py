import logging
import pyo
from shakersynth.config import config

log = logging.getLogger(__name__)
log.setLevel(config.log_level)


class RotorSynth():
    def __init__(self):
        envelope0 = pyo.CosTable([
            (0000, 0.0),
            (2000, 1.0),
            (4000, 1.0),
            (6000, 0.0),
            (8191, 0.0),
        ])

        envelope1 = pyo.CosTable([
            (1000, 0.0),
            (4000, 1.0),
            (6000, 1.0),
            (8000, 0.0),
            (8191, 0.0),
        ])

        self.is_running = False
        self.lfo = pyo.Metro(time=.25, poly=1).play()

        self.vca0 = pyo.TrigEnv(self.lfo, table=envelope0, dur=0.05, mul=0.0)
        self.vca1 = pyo.TrigEnv(self.lfo, table=envelope1, dur=0.05, mul=0.0)
        self.osc0 = pyo.Sine(freq=config.rotor_hz, mul=self.vca0)
        self.osc1 = pyo.Sine(freq=config.rotor_hz, mul=self.vca1)
        self.filter0 = pyo.Biquad(self.osc0, freq=160.0)
        self.filter1 = pyo.Biquad(self.osc1, freq=160.0)

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
        blade_period = 1 / blades_per_second

        # Set the synth pulse interval to trigger for each passing blade.
        self.lfo.setTime(blade_period)

        # Get louder, as well as faster with rising rotor RPM, with a
        # fractional exponential curve so you can still feel the signal at
        # lower RPMs.
        shake_volume = max(
            ((telemetry["rotor_rpm_percent"] / 100) ** 0.6) - 0.05,
            0
        )

        self.vca0.setMul(shake_volume)
        self.vca1.setMul(shake_volume)

        # Lower RPM means slower blades, so each "shake" should last longer.
        shake_duration = blade_period / 6
        self.vca0.setDur(shake_duration)
        self.vca1.setDur(shake_duration)

    def start(self):
        if self.is_running:
            return
        self.filter0.out(0)
        self.filter1.out(1)
        self.is_running = True

    def stop(self):
        if not self.is_running:
            return
        self.filter0.stop()
        self.filter1.stop()
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

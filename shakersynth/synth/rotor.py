import pyo
from shakersynth.config import config


class RotorSynth():
    def __init__(self, server: pyo.Server):
        self.server = server

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

        self.lfo = pyo.Metro(time=.25, poly=1).play()

        self.vca0 = pyo.TrigEnv(self.lfo, table=envelope0, dur=0.05, mul=0.0)
        self.vca1 = pyo.TrigEnv(self.lfo, table=envelope1, dur=0.05, mul=0.0)
        self.osc0 = pyo.Sine(freq=35, mul=self.vca0)
        self.osc1 = pyo.Sine(freq=35, mul=self.vca1)

        self.osc0.out(0)
        self.osc1.out(1)

    def update(self, telemetry):
        """Update synth parameters based on telemetry."""
        rpm = telemetry["rotor_rpm"]
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
        shake_volume = ((telemetry["rotor_rpm_percent"] / 100) ** 0.6)
        shake_volume *= config.global_volume

        self.vca0.setMul(shake_volume)
        self.vca1.setMul(shake_volume)

        # Lower RPM means slower blades, so each "shake" should last longer.
        shake_duration = blade_period / 6
        self.vca0.setDur(shake_duration)
        self.vca1.setDur(shake_duration)

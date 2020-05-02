import pyo

class RotorSynth():
    def __init__(self, server: pyo.Server):
        self.server = server

        envelope = pyo.CosTable([
            (0000, 0.0),
            (2000, 1.0),
            (4000, 1.0),
            (6000, 0.0),
            (8191, 0.0),
        ])

        self.lfo = pyo.Metro(time=.25, poly=1).play()
        self.vca = pyo.TrigEnv(self.lfo, table=envelope, dur=0.05, mul=0.0)
        self.osc = pyo.Sine(freq=35, mul=self.vca)

        self.osc.out()

    def update(self, telemetry):
        """Update synth parameters based on telemetry."""
        rpm = telemetry["rotor_rpm"]
        # Revolutions per _second_ is better as a synth parameter.
        revolutions_per_second = rpm / 60.0

        # The rotor has 5 blades.
        blades_per_second = 5.0 * revolutions_per_second
        blade_period = 1.0 / blades_per_second

        # Set the synth pulse interval to trigger for each passing blade.
        self.lfo.setTime(blade_period)

        # Get louder, as well as faster with rising rotor RPM.
        # Don't go louder than 1.0 to prevent clipping.
        self.vca.setMul(min((rpm / 200), 1.0))

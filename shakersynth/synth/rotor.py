import logging
import pyo
from shakersynth.config import loader

config = loader.load_config()
log = logging.getLogger(__name__)
log.setLevel(config.log.level)


class RotorSynth():
    """Effect synthesizer for helicopter rotor vibrations.

    This a stereo (2 channel) effect.
    """
    def __init__(self):
        """Create a new RotorSynth."""
        self.is_running = False

        # Create two volume faders which we'll use to control
        # the volume of the effect.
        self.fader0 = pyo.Fader()
        self.fader1 = pyo.Fader()

        # These Lorenz attractors create randomness, which we will use to
        # modulate the signal a little. It adds character and makes the
        # effect feel less repetitive.
        self.lorenz0 = pyo.Lorenz(pitch=0.1)
        self.lorenz0_scaled = pyo.Scale(self.lorenz0, outmin=0.3, outmax=0.9)
        self.lorenz1 = pyo.Lorenz(pitch=0.11)  # Slightly different for stereo.
        self.lorenz1_scaled = pyo.Scale(self.lorenz1, outmin=0.3, outmax=0.9)

        # These are the actual signal sources. Volume is controlled by the
        # fader objects and the "sharpness" of the wave is modulated by the
        # Lorenz attractors.
        self.osc0 = pyo.LFO(
            freq=0.0001,
            sharp=self.lorenz0_scaled,
            mul=self.fader0)
        self.osc1 = pyo.LFO(
            freq=0.0001,
            sharp=self.lorenz1_scaled,
            mul=self.fader1)

        # Then we'll filter the signals so that only low frequencies are
        # sent to the shakers.
        self.filter0 = pyo.Biquad(self.osc0, freq=200)
        self.filter1 = pyo.Biquad(self.osc1, freq=200)

        # Finally, hook the output of the filters up to the sound card's left
        # and right channels.
        self.filter0.out(0)
        self.filter1.out(1)

    def update(self, telemetry: dict) -> None:
        """Update synth parameters based on `telemetry`.

        Each time `update` is called with a `telemetry` payload, the
        `RotorSynth` will adjust its synthesis parameters to match.

        `telemetry` must contain the key `rotor_rpm_percent` to have
        any effect.

        Supports the Mi-8, Mi-24, and UH-1H modules.
        """
        module = telemetry["module"]
        if(module == "mi-8mt" or module == "mi-24p"):
            blade_count = 5
        elif(module == "uh-1h"):
            blade_count = 2
        else:
            raise NotImplementedError

        rpm = self._calculate_rotor_rpm(telemetry)

        # Protect against divide-by-zero errors.
        if rpm == 0:
            rpm = 0.00000001

        # Revolutions per second is more useful than RPM.
        revolutions_per_second = rpm / 60.0

        blades_per_second = revolutions_per_second * blade_count
        log.debug(f"blades_per_second: {blades_per_second}")
        self.osc0.setFreq(blades_per_second)
        self.osc1.setFreq(blades_per_second)

        # Only apply the Lorenz attractor "pixie dust" when the
        # rotor is actually moving.
        log.debug(f"Lorenz min: {min(0.3, blades_per_second)}")
        log.debug(f"Lorenz max: {min(0.9, blades_per_second)}")
        self.lorenz0_scaled.setOutMin(min(0.3, blades_per_second))
        self.lorenz0_scaled.setOutMax(min(0.9, blades_per_second))
        self.lorenz1_scaled.setOutMin(min(0.3, blades_per_second))
        self.lorenz1_scaled.setOutMax(min(0.9, blades_per_second))

    def start(self) -> None:
        """Start the `RotorSynth`, activating audio output."""
        if self.is_running:
            return
        log.debug("Started.")
        self.fader0.play()
        self.fader1.play()
        self.is_running = True

    def stop(self) -> None:
        """Stop the `RotorSynth`, deactivating audio output."""
        if not self.is_running:
            return
        log.debug("Stopped.")
        self.fader0.stop()
        self.fader1.stop()
        self.is_running = False

    def _calculate_rotor_rpm(self, telemetry: dict) -> float:
        """Given a telemetry payload, return the true RPM of the rotor."""
        module = telemetry["module"]
        rpm_percent = telemetry["rotor_rpm_percent"]

        if(module == "mi-8mt"):
            # 95 gauge RPM == 192 real rotor RPM. [1, 2]
            # But 200 gives better results in the sim.
            return float(rpm_percent * (200 / 95))
        elif(module == "mi-24p"):
            # 280 gives good sync on the Hind, but that seems way off??
            return float(rpm_percent * (280 / 95))
        elif(module == "uh-1h"):
            # 90 gauge RPM == 324 real rotor RPM. [3]
            return float(rpm_percent * (324 / 90))
        else:
            return 0.00000001

# 1. http://koavia.com/eng/product/helicopter/hvostovye_valy.shtml#2
# 2. https://www.pprune.org/rotorheads/221789-mil-8-mtv-mtv-1-info.html
# 3. https://apps.dtic.mil/dtic/tr/fulltext/u2/901787.pdf

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
    def __init__(self, module: str):
        """Create a new RotorSynth.

        `module` is the lower-case module name, like "mi-8mt".

        Supports the "mi-8mt", "mi-24p", and "uh-1h" modules.
        """
        if module not in ["mi-8mt", "mi-24p", "uh-1h"]:
            raise ValueError
        self.module = module

        self.is_running = False

        # Create two volume faders which we'll use to control
        # the volume of the effect.
        self.faders = [pyo.Fader(), pyo.Fader()]

        # These Lorenz attractors create randomness, which we will use to
        # modulate the signal a little. It adds character and makes the
        # effect feel less repetitive.
        #
        # Make them slightly different to produce stereo.
        self.lorenz = [pyo.Lorenz(pitch=0.1), pyo.Lorenz(pitch=0.11)]

        # The raw lorenz attractors are too strong. Wrap them in scaling
        # functions and use the scaled versions as our final modulation
        # sources.
        self.modulators = [
            pyo.Scale(lorenz, outmin=0.3, outmax=0.9)
            for lorenz in self.lorenz]

        # These are the actual signal sources. Volume is controlled by the
        # fader objects and the "sharpness" of the wave is modulated by the
        # scaled Lorenz attractors.
        self.oscillators = [
            pyo.LFO(freq=0.001, sharp=modulator, mul=fader)
            for modulator, fader in zip(self.modulators, self.faders)]

        # Then we'll filter the signals so that only low frequencies are
        # sent to the shakers.
        self.filters = [pyo.Biquad(osc, freq=200) for osc in self.oscillators]

        # Finally, hook the output of the filters up to the sound card's left
        # and right channels.
        for i in [0, 1]:
            self.filters[i].out(i)

    def update(self, telemetry: dict) -> None:
        """Update synth parameters based on `telemetry`.

        Each time `update` is called with a `telemetry` payload, the
        `RotorSynth` will adjust its synthesis parameters to match.

        `telemetry` must contain the key `rotor_rpm_percent` to have
        any effect.
        """
        if telemetry["module"] != self.module:
            log.error(
                f"Got telemetry for {telemetry['module']}"
                " when running {module}.")
            return

        if(self.module == "mi-8mt" or self.module == "mi-24p"):
            blade_count = 5
        elif(self.module == "uh-1h"):
            blade_count = 2

        rpm_percent = telemetry.get("rotor_rpm_percent", 0)
        rpm = self._calculate_rotor_rpm(rpm_percent)

        # Protect against divide-by-zero errors.
        if rpm == 0:
            rpm = 0.00000001

        # Revolutions per second is more useful than RPM.
        revolutions_per_second = rpm / 60.0

        blades_per_second = revolutions_per_second * blade_count
        [osc.setFreq(blades_per_second) for osc in self.oscillators]

        # Only apply the Lorenz attractor "pixie dust" when the
        # rotor is actually moving.
        [modulator.setOutMin(min(0.3, blades_per_second))
            for modulator in self.modulators]
        [modulator.setOutMax(min(0.9, blades_per_second))
            for modulator in self.modulators]

    def start(self) -> None:
        """Start the `RotorSynth`, activating audio output."""
        if not config.modules[self.module].effects.rotor.enabled:
            return
        if self.is_running:
            return
        log.debug("Started.")
        [fader.play() for fader in self.faders]
        self.is_running = True

    def stop(self) -> None:
        """Stop the `RotorSynth`, deactivating audio output."""
        if not self.is_running:
            return
        log.debug("Stopped.")
        [fader.stop() for fader in self.faders]
        self.is_running = False

    def _calculate_rotor_rpm(self, rpm_percent: float) -> float:
        """Given `rpm_percent` return the true RPM of the rotor."""
        if(self.module == "mi-8mt"):
            # 95 gauge RPM == 192 real rotor RPM. [1, 2]
            # But 200 gives better synchronization in the sim.
            return float(rpm_percent * (200 / 95))
        elif(self.module == "mi-24p"):
            # 280 gives good sync on the Hind.
            return float(rpm_percent * (280 / 95))
        elif(self.module == "uh-1h"):
            # 90 gauge RPM == 324 real rotor RPM. [3]
            return float(rpm_percent * (324 / 90))
        else:
            return 0.00000001

# 1. http://koavia.com/eng/product/helicopter/hvostovye_valy.shtml#2
# 2. https://www.pprune.org/rotorheads/221789-mil-8-mtv-mtv-1-info.html
# 3. https://apps.dtic.mil/dtic/tr/fulltext/u2/901787.pdf

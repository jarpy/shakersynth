import logging

import pyo  # type: ignore

from collections import deque
from statistics import median, mean, mode
from shakersynth.config import loader
from shakersynth.synth.synth import Synth

config = loader.load_config()
log = logging.getLogger(__name__)
log.setLevel(config.log.level)


class GunSynth(Synth):
    """Effect synthesizer for automatic guns."""
    def __init__(self, module: str):
        """Create a new GunSynth.

        `module` is the lower-case module name, like "mi-8mt".

        """

        # We need to keep track of how many rounds are remaining, but we don't
        # know what the initial condition is until we get our first telemetry
        # packet.
        self.ammo_count = None
        self.time = None
        self.rof_history: deque[int] = deque()

        #if module not in ["mi-8mt", "mi-24p", "uh-1h"]:
        #    raise ValueError
        self.module = module
        self.is_running = False

        # Create a volume fader which we'll use to control
        # the volume of the effect.
        self.fader = pyo.Fader()

        # These Lorenz attractors create randomness, which we will use to
        # modulate the signal a little. It adds character and makes the effect
        # feel less repetitive.
        #
        # Make them slightly different to produce stereo.
        self.lorenz = pyo.Lorenz(pitch=[0.10, 0.11])

        # The raw lorenz attractors are too strong. Wrap them in scaling
        # functions and use the scaled versions as our final modulation
        # sources.
        self.modulators = pyo.Scale(self.lorenz, outmin=0.3, outmax=0.9)

        # These are the actual signal sources. Volume is controlled by the
        # fader objects and the "sharpness" of the wave is modulated by the
        # scaled Lorenz attractors.
        self.oscillators = pyo.LFO(
            type=1,
            sharp=0.8,
            freq=[0.001, 0.001], mul=self.fader)

        # Then we'll filter the signals so that only low frequencies are
        # sent to the shakers.
        self.filters = pyo.Biquad(self.oscillators, freq=2000)

        # Finally, hook the output of the filters up to the sound card's left
        # and right channels.
        self.filters.out()

    def update(self, telemetry: dict) -> None:
        """Update synth parameters based on `telemetry`.

        Each time `update` is called with a `telemetry` payload, the `GunSynth`
        will adjust its synthesis parameters to match.

        `telemetry` must contain the key `gun_rounds` to have any effect.
        """
        if telemetry["module"] != self.module:
            log.error(
                f"Got telemetry for {telemetry['module']}"
                " when running {module}.")
            return

        if not self.ammo_count:
            self.ammo_count = telemetry["gun_rounds"]

        if not self.time:
            self.time = telemetry["time"]
            return

        if telemetry["gun_rounds"] < self.ammo_count:
            last_time = self.time
            self.time = telemetry["time"]
            if self.is_running:
                elapsed = telemetry["time"] - last_time
                rof = (self.ammo_count - telemetry["gun_rounds"]) / elapsed
                if int(rof) < 2:
                    return

                self.rof_history.append(int(rof))
                if len(self.rof_history) > 10:
                    self.rof_history.popleft()
                average_rof = median(self.rof_history)
                # self.oscillators.setFreq(average_rof)
                self.oscillators.setFreq(160)
                self.ammo_count = telemetry["gun_rounds"]
                self.fader.setFadein(0.01)
                self.fader.setFadeout(2 / average_rof)

            self.start()
        else:
            self.stop()


        # Only apply the Lorenz attractor "pixie dust" when the rotor is
        # actually moving. Otherwise, the attractors themselves produce enough
        # noise to be noticeable before the chopper starts up.
        self.modulators.setOutMin(min(0.3, 0))
        self.modulators.setOutMax(min(0.9, 0))

    def start(self) -> None:
        """Start the `GunSynth`, activating audio output."""
        if self.is_running:
            return
        #if not config.modules[self.module].effects.rotor.enabled:
        #    return
        log.debug(f"Started {self}.")
        self.fader.play()
        self.is_running = True

    def stop(self) -> None:
        """Stop the `RotorSynth`, deactivating audio output."""
        if not self.is_running:
            return
        log.debug(f"Stopped {self}.")
        self.fader.stop()
        self.is_running = False

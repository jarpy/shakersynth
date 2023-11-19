import logging
import pyo
from shakersynth.config import loader

config = loader.load_config()
log = logging.getLogger(__name__)
log.setLevel(config.log.level)


class BumpSynth:
    """ simple synthesizer for single-shot bumps, impacts and alike"""

    def __init__(self, module: str):
        """ we support ALL modules.
        if there's telemetry - thou shallest bump! """

        self.module = module
        self.is_running = False

        # fader to control the volume-envelope of the effect
        self.env = pyo.Fader(fadein=.01, fadeout=.1, dur=.11)
        # as well as a low-frequency-oscilator to get things swinging
        self.osc = pyo.LFO(freq=[1, 1], mul=self.env)
        # and finally - a low pass, to protect our shakers
        filters = pyo.Biquad(self.osc, freq=200).out()

        self.total_ammo_last = 0
        self.doors_open_last = 0

    def start(self) -> None:
        """Start the `BumpSynth`, activating audio output."""
        if self.is_running:
            return
        if not config.modules[self.module].effects.bump.enabled:
            return
        log.debug("BumpSynth Started.")
        self.is_running = True

    def update(self, telemetry: dict) -> None:

        # TODO: not sure how this could even happen, but left it in for now
        if telemetry["module"] != self.module:
            log.error(
                f"Got telemetry for {telemetry['module']} when running {self.module}.")
            return

        if 'ammo' in telemetry:
            # process ammo - simply watch for changes in count
            total_ammo = sum(telemetry['ammo'])
            total_ammo_change = total_ammo - self.total_ammo_last
            if total_ammo_change != 0:
                self.total_ammo_last = total_ammo
                log.debug(f"ammo count changed to: %d" % total_ammo)
                if total_ammo_change > 0:
                    log.debug(f"loaded %d more ammo." % total_ammo_change)
                else:
                    log.debug(f"used %d ammo." % -total_ammo_change)
                    self._play_bump(40,0.01,0.02)  # very small bump, this is just WiP

        if 'doors' in telemetry:
            # process doors - everything >0 counts as open
            doors_open = sum(map(lambda x: x > 0, telemetry['doors']))
            doors_open_change = doors_open - self.doors_open_last
            if doors_open_change != 0:
                self.doors_open_last = doors_open
                if doors_open_change > 0:
                    log.debug(f"%d doors opened." % doors_open_change)
                    self._play_bump(50,0.01,0.03)  # small bump - just unlocking the door
                else:
                    log.debug(f"%d doors closed." % -doors_open_change)  # big bump
                    self._play_bump(44,0.01,0.1)  # medium impact, door connects to the fuselage

    def stop(self) -> None:
        """Stop the `BumpSynth`, deactivating audio output."""
        if not self.is_running:
            return
        log.debug("BumpSynth Stopped.")
        self.env.stop()
        self.is_running = False

    def _play_bump(self, freq=40, attack=0.01, release=0.1):
        self.osc.freq = [freq, freq * 1.001]
        self.env.fadein = attack
        self.env.fadeout = release
        self.env.play()

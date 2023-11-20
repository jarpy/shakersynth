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

        # AR envelope to control the volume of the effect
        self.env = pyo.Adsr(decay=0, sustain=1)
        self.env.setExp(1.2)
        # as well as a low-frequency-oscilator to get things swinging
        self.osc = pyo.LFO(freq=[1, 1], mul=self.env)
        # and finally - a low pass, to protect our shakers
        self.filters = pyo.Biquad(self.osc, freq=200)
        self.filters.out()

        self.total_ammo_last = None
        self.doors_open_last = None

    def start(self) -> None:
        """Start the `BumpSynth`, activating audio output."""
        if self.is_running:
            return
        if not config.modules[self.module].effects.bump.enabled:
            return
        log.debug("Started.")
        self.is_running = True

    def stop(self) -> None:
        """Stop the `BumpSynth`, deactivating audio output."""
        if not self.is_running:
            return
        log.debug("Stopped.")
        self.is_running = False

    def update(self, telemetry: dict) -> None:

        # TODO: not sure how this could even happen, but left it in for now
        if telemetry["module"] != self.module:
            log.error(
                f"Got telemetry for {telemetry['module']} when running {self.module}.")
            return

        if 'ammo' in telemetry:
            # process ammo - simply watch for changes in count
            total_ammo = sum(telemetry['ammo'])
            if self.total_ammo_last is not None:
                total_ammo_change = total_ammo - self.total_ammo_last
                if total_ammo_change != 0:
                    if total_ammo_change > 0:
                        log.debug(f"loaded %d more ammo." % total_ammo_change)
                        self._play_bump(0.7, 0.01, 0.1)  # medium impact, something connected to the fuselage
                    else:
                        log.debug(f"used %d ammo." % -total_ammo_change)
                        self._play_bump(0.7, 0.01, 0.02)  # short spike
            self.total_ammo_last = total_ammo

        if 'doors' in telemetry:
            # process doors - everything >0 counts as open
            doors_open = sum(map(lambda x: x > 0, telemetry['doors']))
            if self.doors_open_last is not None:
                doors_open_change = doors_open - self.doors_open_last
                if doors_open_change != 0:
                    if doors_open_change > 0:
                        log.debug(f"%d doors opened." % doors_open_change)
                        self._play_bump(0.6, 0.01, 0.05)  # small bump - just unlocking the door
                    else:
                        log.debug(f"%d doors closed." % -doors_open_change)  # big bump
                        self._play_bump(0.8, 0.01, 0.1)  # medium impact, door connects to the fuselage
            self.doors_open_last = doors_open

    def _play_bump(self, volume: float=1.0, attack: float=0.01, release: float=0.1, freq: float=45.0) -> None:
        log.debug(f"playing a %.1fHz bump with vol=%.2f A=%.2f R=%.2f" % (freq, volume, attack, release))
        self.osc.freq = [freq, freq * .998]
        self.env.attack = attack
        self.env.release = release
        self.env.dur = attack + release
        self.env.mul = volume
        self.env.play()

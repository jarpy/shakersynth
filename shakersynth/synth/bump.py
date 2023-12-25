import logging
import pyo  # type: ignore
from shakersynth.config import loader
from typing import Optional

config = loader.load_config()
log = logging.getLogger(__name__)
log.setLevel(config.log.level)


class BumpSynth:
    """Simple synthesizer for single-shot bumps, impacts, and the like."""

    def __init__(self, module: str):
        # We support ALL modules.
        # If there's telemetry, thou shallest bump!

        self.module = module
        self.is_running = False

        # Envelope to control the volume of the effect.
        self.env = pyo.Adsr(decay=0, sustain=1)
        self.env.setExp(1.2)
        # As well as a Low Frequency Oscillator to get things swinging.
        # This is actually a pair of oscillators, so we can generate
        # stereo effects.
        self.osc = pyo.LFO(freq=[1, 1], mul=self.env)
        # And finally, a low pass filter to protect our shakers from high frequencies.
        self.filters = pyo.Biquad(self.osc, freq=200)
        self.filters.out()

        # Tracking variables so we can compare the state of things
        # in the current payload to previous state.
        self.total_ammo_last: Optional[bool] = None
        self.doors_open_last: Optional[bool] = None

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
        """Process telemetry, emitting bumps for supported events."""
        if telemetry["module"] != self.module:
            # This can happen when restarting DCS after a crash.
            log.error(
                f"Got telemetry for {telemetry['module']} when running {self.module}."
            )
            return

        if "ammo" in telemetry:
            # Process ammo. Simply watch for changes in count.
            total_ammo = sum(telemetry["ammo"])
            if self.total_ammo_last is not None:
                total_ammo_change = total_ammo - self.total_ammo_last
                if total_ammo_change != 0:
                    if total_ammo_change > 0:
                        log.debug(f"Loaded {total_ammo_change} ammo.")
                        # Medium impact, something connected to the fuselage.
                        self._play_bump(0.7, 0.01, 0.1)
                    else:
                        log.debug(f"Used {total_ammo_change} ammo.")
                        # Short spike.
                        self._play_bump(0.7, 0.01, 0.02)
            self.total_ammo_last = total_ammo

        if "doors" in telemetry:
            # Process all doors. Everything >0 counts as open.
            doors_open = any(door > 0 for door in telemetry["doors"])
            if self.doors_open_last is not None:
                doors_open_change = doors_open - self.doors_open_last
                if doors_open_change != 0:
                    if doors_open_change > 0:
                        log.debug(f"{doors_open_change} doors opened.")
                        # Small bump. Just opening the door.
                        self._play_bump(0.6, 0.01, 0.05)
                    else:
                        # Big bump. Closing a door should be satisfying.
                        log.debug(f"{-doors_open_change} doors closed.")
                        self._play_bump(0.8, 0.01, 0.1)
            self.doors_open_last = doors_open

    def _play_bump(
        self,
        volume: float = 1.0,
        attack: float = 0.01,
        release: float = 0.1,
        freq: float = 45.0,
    ) -> None:
        """Emit a bump effect."""
        log.debug(
            f"Playing a {freq:.1f}Hz bump with vol={volume:.2f} A={attack:.2f} R={release:.2f}"
        )
        # Set a slight difference in the frequencies of the dual oscillators,
        # to add some stereo character.
        self.osc.freq = [freq, freq * 0.998]
        self.env.attack = attack
        self.env.release = release
        self.env.dur = attack + release
        self.env.mul = volume
        self.env.play()

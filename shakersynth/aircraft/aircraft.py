import logging
from shakersynth.synth.rotor import RotorSynth
from shakersynth.config import config
from typing import Dict  # noqa: F401

log = logging.getLogger(__name__)
log.setLevel(config.log_level)


class Aircraft:
    """An `Aircraft` is the current aircraft/module the player is controlling.

    The `Aircraft` contains instances of `shakersynth.synth` in a list.
    Calling `update` on the `Aircraft` causes each synth to also be updated.
    """
    def __init__(self):
        """Create a new `Aircraft, with a collection of synths."""
        self.synths = [RotorSynth()]
        self.is_running = False

    def update(self, telemetry: dict):
        """Update all synths with the `telemetry` payload."""
        for synth in self.synths:
            try:
                synth.update(telemetry)
            except NotImplementedError:
                module = telemetry["module"]
                log.debug(
                    "%s module not supported by %s" % (module, type(synth)))

    def start(self):
        """Start all synths, enabling audio output."""
        for synth in self.synths:
            log.debug("Starting synth: %s" % type(synth))
            synth.start()
        self.is_running = True

    def stop(self):
        """Stop all synths, disabling audio output."""
        for synth in self.synths:
            log.debug("Stopping synth: %s" % type(synth))
            synth.stop()
        self.is_running = False

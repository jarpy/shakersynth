import logging
from shakersynth.synth.rotor import RotorSynth
from shakersynth.config import loader
from typing import Dict  # noqa: F401

config = loader.load_config()
log = logging.getLogger(__name__)
log.setLevel(config.log.level)

helicopters = ['mi-8mt', 'mi-24p', 'uh-1h']
fixed_wings = ['a10-c_2']
all_modules = helicopters + fixed_wings


class Aircraft:
    """An `Aircraft` is the current aircraft/module the player is controlling.

    The `Aircraft` contains instances of `shakersynth.synth` in a list.
    Calling `update` on the `Aircraft` causes each synth to also be updated.
    """
    def __init__(self, module: str):
        """Create a new `Aircraft`, with a collection of synths."""
        self.module = module
        self.synths = []
        self.is_running = False

        if module in helicopters:
            if config.modules[module].effects.rotor.enabled:
                self.synths.append(RotorSynth())
            else:
                log.info(f"Rotor effect disabled for {module}.")

    def update(self, telemetry: dict) -> None:
        """Update all synths with the `telemetry` payload."""
        for synth in self.synths:
            try:
                synth.update(telemetry)
            except NotImplementedError:
                log.error(f"{type(synth)}: unsupported module '{self.module}'")

    def start(self) -> None:
        """Start all synths, enabling audio output."""
        for synth in self.synths:
            log.debug("Starting synth: %s" % type(synth))
            synth.start()
        self.is_running = True

    def stop(self) -> None:
        """Stop all synths, disabling audio output."""
        for synth in self.synths:
            log.debug("Stopping synth: %s" % type(synth))
            synth.stop()
        self.is_running = False

import logging
from shakersynth.synth.rotor import RotorSynth
from shakersynth.synth.bump import BumpSynth
from shakersynth.config import loader

config = loader.load_config()
log = logging.getLogger(__name__)
log.setLevel(config.log.level)

synth_map: dict = {
    "a10-c_2": [],
    "mi-24p": [RotorSynth, BumpSynth],
    "mi-8mt": [RotorSynth, BumpSynth],
    "ka-50": [RotorSynth, BumpSynth],
    "uh-1h": [RotorSynth, BumpSynth],
}


class Aircraft:
    """An `Aircraft` is the current aircraft/module the player is controlling.

    The `Aircraft` contains instances of `shakersynth.synth` in a list.
    Calling `update` on the `Aircraft` causes each synth to also be updated.
    """
    def __init__(self, module: str):
        """Create a new `Aircraft`, with a collection of synths.

        Only synths that are relevant to the module are added. For example,
        helicopters receive a `RotorSynth`, but fixed-wing aircraft do not.
        """
        self.module = module
        self.synths = [Synth(module) for Synth in synth_map.get(module, [])]
        self.is_running = False

    def start(self) -> None:
        """Start all synths, enabling audio output."""
        [synth.start() for synth in self.synths]
        self.is_running = True

    def stop(self) -> None:
        """Stop all synths, disabling audio output."""
        [synth.stop() for synth in self.synths]
        self.is_running = False

    def update(self, telemetry: dict) -> None:
        """Update all synths with the `telemetry` payload."""
        [synth.update(telemetry) for synth in self.synths]

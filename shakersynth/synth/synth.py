from abc import ABC, abstractmethod


class Synth(ABC):
    """Abstract base class for all effect synthesizers.

    Defines the API that a synth must implement.
    """
    @abstractmethod
    def update(self, telemetry: dict) -> None:
        """Update synth parameters based on `telemetry`."""

    @abstractmethod
    def start(self) -> None:
        """Turn on the effect."""

    @abstractmethod
    def stop(self) -> None:
        """Turn off the effect."""

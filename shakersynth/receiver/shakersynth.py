import logging
import socket
import yaml
from func_timeout import func_set_timeout, FunctionTimedOut  # type: ignore
from shakersynth.config import loader

config = loader.load_config()
log = logging.getLogger(__name__)
log.setLevel(config.log.level)


class ShakersynthReceiver():
    """Receive YAML encoded telemetry from Shakersynth's DCS export script."""

    def __init__(self, bind_addr="", port=17707):
        """Create a `ShakersynthReceiver` listening on a UDP socket.

        If `port` is `None`, no socket will be opened. Useful when the
        `ShakersynthReceiver` is under test."""
        self.packet_count = 0
        if port is not None:
            self.listener = socket.socket(type=socket.SOCK_DGRAM)
            self.listener.bind((bind_addr, port))

    @func_set_timeout(1)
    def _receive_udp(self) -> bytes:
        """Receive a UDP packet.

        Raises FunctionTimedOut if one is not received within 1 second.
        """
        return self.listener.recv(1500)

    def receive(self) -> dict:
        """Return the next available telemetry payload.

        Returns an empty dictionary if nothing is received within 1 second.
        """
        try:
            payload = self._receive_udp()
            self.packet_count += 1
        except FunctionTimedOut:
            log.debug('No telemetry...')
            return {}

        # YAML may seem like a strange wire format, but it's very fast and
        # clean to hand-craft it in the export script. Decoding it may be
        # relatively expensive, but we have cycles to spare here in the Python
        # world.
        telemetry = yaml.safe_load(payload.decode())

        # Capital letters hurt your hands.
        try:
            telemetry["module"] = telemetry["module"].lower()
        except KeyError:
            # No module is active. Return an empty telemetry object signifying
            # that we are not currently in an aircraft.
            return {}

        if self.packet_count % 60 == 0:
            log.debug("Telemetry sample: %s" % telemetry)
        return telemetry

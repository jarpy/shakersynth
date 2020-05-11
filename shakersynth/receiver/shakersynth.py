import socket
import yaml


class ShakersynthReceiver():
    """Recieve YAML encoded telemetry from Shakersynth's DCS export script."""

    def __init__(self, bind_addr="localhost", port=17707):
        """Create a telemetry receiver listening on a UDP socket."""
        if port is not None:
            self.listener = socket.socket(type=socket.SOCK_DGRAM)
            self.listener.bind((bind_addr, port))

    def get_telemetry(self):
        """Return the next available telemetry payload.

        Blocks until one is available.
        """
        # TODO: Put a time-out around this so that we'll return an empty
        # payload if DCS stops transmitting. An emtpy payload will shut down
        # the synth engine, so it's like a "dead man's handle".
        message = self.listener.recv(1500)

        # YAML may seem like a strange wire format, but it's very fast and
        # clean to hand-craft it in the export script. Decoding it may be
        # relatively expensive, but we have cycles to spare here in the Python
        # world.
        telemetry = yaml.safe_load(message.decode())

        # Capital letters hurt your hands.
        module = telemetry["module"].lower()

        if module == "mi-8mt":  # Nobody says "Mi-8MT".
            module = "mi-8"     # We just say "Mi-8".

        telemetry["module"] = module

        return telemetry

import socket


class SimShakerReceiver():
    def __init__(self, port=29377):
        if port is not None:
            self.listener = socket.socket(type=socket.SOCK_DGRAM)
            self.listener.bind(('', port))

    def get_telemetry(self):
        """Return the next available telemetry payload.

        Blocks until one is available.
        """
        message = self.listener.recv(1500)
        simshaker = self.parse(message.decode())

        telemetry = {}

        # Module name
        try:
            module = simshaker["N"].lower()
        except KeyError:
            # Not a telemetry packet from SimShaker.
            # Probably a "start" or "stop" message.
            return {}
        if module == "mi-8mt":
            telemetry["module"] = "mi-8"
        else:
            telemetry["module"] = module

        # Rotor RPM
        try:
            rpm_percent = float(simshaker["RotorRPM"])
        except KeyError:
            rpm_percent = 0.0
        telemetry["rotor_rpm_percent"] = rpm_percent

        return telemetry

    def parse(self, message):
        """Parse a SimShaker telemetry message into a dict."""
        simshaker_telemetry = {}
        elements = message.split(';')

        for element in elements:
            try:
                key, value = element.split("=")
                simshaker_telemetry[key] = value
            except ValueError:
                pass

        return simshaker_telemetry

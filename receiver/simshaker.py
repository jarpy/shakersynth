import socket
import os
import json

class SimShakerReceiver():
    def __init__(self):
        self.listener = socket.socket(type=socket.SOCK_DGRAM)
        self.listener.bind(('localhost', 29377))
        self.counter = 0

    def get_telemetry(self):
        """Return the next available telemetry payload.

        Blocks until one is available.
        """
        telemetry = {}
        message = self.listener.recv(1500)
        simshaker = self.parse(message.decode())

        try:
            gauge_rpm = float(simshaker["RotorRPM"])
        except KeyError:
            gauge_rpm = 0.0

        # Protect against divide by zero.
        gauge_rpm = max(gauge_rpm, 0.0000001)

        # 95 gauge RPM == 192 real rotor RPM.
        # REF: http://koavia.com/eng/product/helicopter/hvostovye_valy.shtml#2
        # REF: https://www.pprune.org/rotorheads/221789-mil-8-mtv-mtv-1-info.html
        real_rpm = gauge_rpm * 2.02105
        telemetry["rotor_rpm"] = real_rpm
        return telemetry

    def parse(self, message):
        """Parse a SimShaker telemetry message into a dict."""
        simshaker_telemetry = {}
        elements = message.split(';')
        if self.counter == 0:
            os.system("cls")
            for element in elements:
                print(element)

        if self.counter == 60:
            self.counter = 0
        else:
            self.counter += 1

        for element in elements:
            try:
                key, value = element.split("=")
                simshaker_telemetry[key] = value
            except ValueError:
                pass
        return simshaker_telemetry

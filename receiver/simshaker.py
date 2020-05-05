import socket
import os
import json
import platform


class SimShakerReceiver():
    def __init__(self):
        self.listener = socket.socket(type=socket.SOCK_DGRAM)
        self.listener.bind(('localhost', 29377))
        self.counter = 0

    def get_telemetry(self):
        """Return the next available telemetry payload.

        Blocks until one is available.
        """
        message = self.listener.recv(1500)
        simshaker = self.parse(message.decode())

        telemetry = {}
        try:
            telemetry["module"] = simshaker["N"]
        except KeyError:
            # Not a telemetry packet from SimShaker.
            # Probably a "start" or "stop" message.
            return {}

        telemetry["rotor_rpm"], telemetry["rotor_rpm_percent"] = self.calculate_rotor_rpm(telemetry["module"], simshaker)

        if self.counter == 0:
            print(json.dumps(telemetry, indent=4))
        if self.counter == 60:
            self.counter = 0
        else:
            self.counter += 1

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

        if self.counter == 0:
            if platform.system() == "Windows":
                os.system("cls")
            for element in elements:
                print(element)

        return simshaker_telemetry

    def calculate_rotor_rpm(self, module, simshaker):
        try:
            gauge_rpm = float(simshaker["RotorRPM"])
        except KeyError:
            gauge_rpm = 0.0

        # Protect against divide by zero.
        gauge_rpm = max(gauge_rpm, 0.0000001)

        if(module == "Mi-8"):
            # 95 gauge RPM == 192 real rotor RPM.
            # REF: http://koavia.com/eng/product/helicopter/hvostovye_valy.shtml#2
            # REF: https://www.pprune.org/rotorheads/221789-mil-8-mtv-mtv-1-info.html
            real_rpm = gauge_rpm * 2.02105
            rotor_rpm = real_rpm
        elif(module == "UH-1H"):
            # 90 gauge RPM == 324 real rotor RPM.
            real_rpm = gauge_rpm * 3.6
            rotor_rpm = real_rpm

        return rotor_rpm, gauge_rpm

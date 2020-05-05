import socket
import os
import json
import platform


class SimShakerReceiver():
    def __init__(self, port=29377):
        if port is not None:
            self.listener = socket.socket(type=socket.SOCK_DGRAM)
            self.listener.bind(('localhost', port))
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

        try:
            telemetry["rotor_rpm_percent"] = float(simshaker["RotorRPM"])
        except KeyError:
            telemetry["rotor_rpm_percent"] = 0.00000001

        telemetry["rotor_rpm"] = self.calculate_rotor_rpm(telemetry)

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

    def calculate_rotor_rpm(self, telemetry):
        module = telemetry["module"]
        rpm_percent = telemetry["rotor_rpm_percent"]

        if(module == "Mi-8"):
            # 95 gauge RPM == 192 real rotor RPM.
            # REF: http://koavia.com/eng/product/helicopter/hvostovye_valy.shtml#2
            # REF: https://www.pprune.org/rotorheads/221789-mil-8-mtv-mtv-1-info.html
            rpm = rpm_percent * 2.02105
        elif(module == "UH-1H"):
            # 90 gauge RPM == 324 real rotor RPM.
            rpm = rpm_percent * 3.6

        return rpm

import logging
import platform
import pyo
from shakersynth.aircraft.aircraft import Aircraft
from shakersynth.receiver.simshaker import SimShakerReceiver
from logging import info

logging.basicConfig(level=logging.INFO)

# Audio synthesis setup.
server = pyo.Server(duplex=0)

if platform.system() == "Windows":
    # Running for real with DCS, so ask which sound device has the bass shakers
    # attached.
    print(pyo.pa_list_devices())
    print("Enter device ID: ")
    device_id = int(input())
    server.setOutputDevice(device_id)
else:
    # Developing on Linux, just send to the default device so we can listen
    # on headphones.
    server.setOutputDevice(pyo.pa_get_default_output())

server.boot()
server.start()

# A little state machine
aircraft = None

# Receive Telemetry in SimShaker format (for now).
receiver = SimShakerReceiver()

while True:
    telemetry = receiver.get_telemetry()

    if telemetry and aircraft is None:
        info("Starting new aircraft: %s" % telemetry["module"])
        aircraft = Aircraft(server)
        aircraft.update(telemetry)
    elif telemetry and aircraft:
        aircraft.update(telemetry)
    elif not telemetry:
        info("Shutting down aircraft: %s" % aircraft["module"])
        del(aircraft)  # To stop all attached synths.
        aircraft = None

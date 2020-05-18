#!/usr/bin/env python3

import logging
import platform
import pyo
import sys
from shakersynth.aircraft.aircraft import Aircraft
from shakersynth.receiver.shakersynth import ShakersynthReceiver
from logging import info

logging.basicConfig(level=logging.INFO)


def main():
    # Audio synthesis setup.
    server = pyo.Server(nchnls=2, duplex=0, buffersize=2048)
    server.setVerbosity(1)

    if platform.system() == "Windows":
        # Running for real with DCS, so ask which sound device has the bass
        # shakers attached.
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

    # Receive Telemetry from the Shakersynth DCS export script.
    receiver = ShakersynthReceiver()

    # All telemetry processing and sound synthesis happens in the aircraft
    # model.
    aircraft = Aircraft(synth_engine=server)

    # On Windows, ctrl+c will not stop our process if we are blocked on
    # waiting for a for a UDP packet. However, ctrl+break will.
    if platform.system() == "Windows":
        print("*" * 80)
        print("Press ctrl+break to exit Shakersynth.")
        print("*" * 80)

    # A little state machine to keep track of our aircraft and telemetry.
    while True:
        telemetry = receiver.get_telemetry()

        if telemetry and not aircraft.is_running:
            # Then we have just started a mission.
            info("Starting new aircraft: %s" % telemetry["module"])
            aircraft.update(telemetry)
            aircraft.start()

        elif telemetry and aircraft.is_running:
            # Then things are ticking along nicely.
            aircraft.update(telemetry)

        elif aircraft.is_running and not telemetry:
            # Then we got an empty telemetry object while running an aircraft.
            # This signifies that we left the mission or lost contact with DCS.
            info("Shutting down aircraft: %s" % aircraft["module"])
            aircraft.stop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)

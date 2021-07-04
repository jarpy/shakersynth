#!/usr/bin/env python3

import logging
import pyo
import sys
import time
from shakersynth.config import config
from shakersynth.aircraft.aircraft import Aircraft
from shakersynth.receiver.shakersynth import ShakersynthReceiver

logging.basicConfig()
log = logging.getLogger("main")
log.setLevel(config.log_level)


def main():
    print("\n" + "-" * 35 + "Shakersynth" + "-" * 35)
    # Audio synthesis setup.
    server = pyo.Server(
        nchnls=2,
        duplex=0,
        buffersize=config.buffer_size,
        sr=config.sample_rate
    )
    server.setVerbosity(1)

    # Map audio outputs from internal numbers (which can be sparse and large)
    # to a friendly, 1-indexed, monotonic series for the user.
    print("Scanning audio devices...")
    output_devices = pyo.pa_get_devices_infos()[1]
    default_api = pyo.pa_get_default_host_api()
    friendly_to_internal = {}

    print("Found these audio outputs:")
    device_details = enumerate(output_devices.items())
    for friendly_index, (internal_index, properties) in device_details:
        # Only list devices that are available using the default audio API.
        if properties["host api index"] == default_api:
            friendly_index += 1
            friendly_to_internal[friendly_index] = internal_index
            print(f"  {friendly_index}: {properties['name']}")

    print("Enter device ID to use: ", end="")
    chosen_device = int(input())
    server.setOutputDevice(friendly_to_internal[chosen_device])

    server.boot()
    server.start()
    server.setAmp(config.global_volume)

    # Receive Telemetry from the Shakersynth DCS export script.
    receiver = ShakersynthReceiver()

    print("*" * 80)
    print("ShakerSynth now running.")
    print("Press ctrl+c to exit.")
    print("*" * 80)
    log.info("Waiting for initial telemetry.")

    # A little state machine to keep track of our aircraft and telemetry.
    running = False
    while True:
        telemetry = receiver.receive()

        if telemetry and not running:
            # Then we have just started a mission.
            module = telemetry['module']
            log.info(f"Starting new aircraft: {module}")
            aircraft = Aircraft(module)
            aircraft.start()
            aircraft.update(telemetry)
            running = aircraft.is_running

        elif telemetry and running:
            # Then things are ticking along nicely.
            aircraft.update(telemetry)

        elif running and not telemetry:
            # Then we got an empty telemetry object while running an aircraft.
            # This signifies that we left the mission or lost contact with DCS.
            log.info(f"Shutting down aircraft: {aircraft.module}")
            aircraft.stop()
            running = aircraft.is_running
            time.sleep(0.1)
            del(aircraft)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)

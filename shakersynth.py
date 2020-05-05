import platform
import pyo
from receiver.simshaker import SimShakerReceiver
from synth.rotor import RotorSynth

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

# Receive Telemetry in SimShaker format (for now).
receiver = SimShakerReceiver()

# Create a synthesizer for main rotor vibrations.
rotor = RotorSynth(server)

while True:
    telemetry = receiver.get_telemetry()
    if telemetry:
        rotor.update(telemetry)

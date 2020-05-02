import pyo
from time import sleep
from receiver.simshaker import SimShakerReceiver
from synth.rotor import RotorSynth

# Audio synthesis setup.
print(pyo.pa_list_devices())
print("Enter device ID: ")
device_id = int(input())
server = pyo.Server()
server.setOutputDevice(device_id)
server.boot()
server.start()

receiver = SimShakerReceiver()
rotor = RotorSynth(server)

while True:
    telemetry = receiver.get_telemetry()
    rotor.update(telemetry)

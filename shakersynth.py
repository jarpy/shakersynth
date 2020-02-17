import socket
import pyo


rotor_fundamental_freq = 30
rotor_volume = 0.25

listener = socket.socket(type=socket.SOCK_DGRAM)
listener.bind(('localhost', 29377))

synth = pyo.Server()
synth.setOutputDevice(10)
synth.boot()
synth.start()

t = pyo.CosTable([
  (0000, 0.0),
  (2000, 1.0),
  (4000, 1.0),
  (6000, 0.0),
  (8191, 0.0),
])

met = pyo.Metro(time=.25, poly=1).play()
amp = pyo.TrigEnv(met, table=t, dur=.05, mul=1)
sin1 = pyo.Sine(freq=35, mul=amp).out()


def parse(message):
    telemetry = {}
    elements = message.split(';')
    for element in elements:
        key, value = element.split("=")
        telemetry[key] = value
    return telemetry


event_counter = 0
while True:
    message, address = listener.recvfrom(1500)
    telemetry = parse(message.decode())

    # REF: http://koavia.com/eng/product/helicopter/hvostovye_valy.shtml#2
    rpm = int(telemetry["RotorRPM"]) * 2
    blade_interval = ((1/rpm * 10))

    met.setTime(blade_interval)

    if event_counter == 0:
        print("Gauge RPM: %s" % telemetry["RotorRPM"])
        print("Real RPM: %s" % rpm)
        print("Rotor mod interval: %s" % blade_interval)
        print("Rotor mod hz: %s" % (1/blade_interval))

    event_counter += 1

    if event_counter == 100:
        event_counter = 0

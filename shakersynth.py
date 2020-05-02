import socket
import pyo
from time import sleep

# Network setup.0
listener = socket.socket(type=socket.SOCK_DGRAM)
listener.bind(('localhost', 29377))

# Audio synthesis setup.
print(pyo.pa_list_devices())
print("Enter device ID: ")
device_id = int(input())
synth = pyo.Server()
synth.setOutputDevice(device_id)
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
amp = pyo.TrigEnv(met, table=t, dur=0.05, mul=0.0)
sin1 = pyo.Sine(freq=35, mul=amp).out()


def parse(message):
    """Parse a SimShaker telemetry message into a dict."""
    telemetry = {}
    elements = message.split(';')
    for element in elements:
        try:
            key, value = element.split("=")
            telemetry[key] = value
        except ValueError:
            pass
    return telemetry


event_counter = 0
while True:
    message, address = listener.recvfrom(1500)
    telemetry = parse(message.decode())

    try:
        gauge_rpm = float(telemetry["RotorRPM"])
    except KeyError:
        gauge_rpm = 0.0

    # No RotorRPM or it's so low that we should just stay silent.
    # Also protects against divide-by-zero when we start doing maths.
    if gauge_rpm < 0.1:
        amp.setMul(0)
        continue

    # 95 gauge RPM == 192 real rotor RPM.
    # REF: http://koavia.com/eng/product/helicopter/hvostovye_valy.shtml#2
    # REF: https://www.pprune.org/rotorheads/221789-mil-8-mtv-mtv-1-info.html
    real_rpm = gauge_rpm * 2.02105

    # Revolutions per _second_ is better as a synth parameter.
    revolutions_per_second = real_rpm / 60.0

    # The rotor has 5 blades.
    blades_per_second = 5.0 * revolutions_per_second

    # Set the synth pulse interval to trigger for each passing blade.
    blade_interval = 1.0 / blades_per_second
    met.setTime(blade_interval)

    # Get louder, as well as faster with rising rotor RPM.
    # Don't go louder than 1.0 to prevent clipping.
    amp.setMul(min((gauge_rpm / 100.0), 1.0))

    # Debug printing
    if event_counter == 0:
        print("Gauge RPM: %s" % gauge_rpm)
        print("Real RPM: %s" % real_rpm)
        print("Rotor mod interval: %s" % blade_interval)
        print("Rotor mod hz: %s" % (1 / blade_interval))
    event_counter += 1
    if event_counter == 100:
        event_counter = 0

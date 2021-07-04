import yaml
import socket
from time import sleep


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def transmit(telemetry: dict):
    payload = yaml.dump(telemetry)
    sock.sendto(payload.encode(), ("127.0.0.1", 17707))


while True:
    print("Starting module we don't support.")
    for n in range(0, 2):
        transmit({
            "module": "ornithopter",
        })
        sleep(1/240)
    transmit({})
    sleep(2)

    print("Starting glorious Mi-8, Commander!")
    rotor_rpm_percent = 0.01
    for n in range(0, 2000):
        transmit({
            "module": "Mi-8MT",
            "rotor_rpm_percent": rotor_rpm_percent,
        })
        if rotor_rpm_percent < 95:
            rotor_rpm_percent += 0.05
        sleep(1/240)
    transmit({})
    sleep(2)

    print("Starting fearsome Mi-24, Comrade!")
    rotor_rpm_percent = 0.01
    for n in range(0, 2000):
        transmit({
            "module": "Mi-24P",
            "rotor_rpm_percent": rotor_rpm_percent,
        })
        if rotor_rpm_percent < 95:
            rotor_rpm_percent += 0.05
        sleep(1/240)
    transmit({})
    sleep(2)

    print("Starting wimpy little toy helicopter from America.")
    rotor_rpm_percent = 0.01
    for n in range(0, 2000):
        transmit({
            "module": "UH-1H",
            "rotor_rpm_percent": rotor_rpm_percent,
        })
        if rotor_rpm_percent < 90:
            rotor_rpm_percent += 0.05
        sleep(1/240)
    transmit({})
    sleep(2)

    print("Starting the awesome Hog!")
    rotor_rpm_percent = 0.01
    for n in range(0, 2000):
        transmit({
            "module": "A10-C_2",
            "rotor_rpm_percent": rotor_rpm_percent,
        })
        if rotor_rpm_percent < 90:
            rotor_rpm_percent += 0.05
        sleep(1/240)
    transmit({})
    sleep(2)

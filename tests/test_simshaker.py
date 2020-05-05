from shakersynth.receiver.simshaker import SimShakerReceiver
from pytest import fixture

mi8_packet = """T=35.34;N=Mi-8;RotorRPM=95;"""
huey_packet = """T=35.34;N=UH-1H;RotorRPM=90;"""


@fixture
def receiver():
    return SimShakerReceiver(port=None)


def test_parse_returns_rotor_rpm_as_a_string(receiver):
    telemetry = receiver.parse(mi8_packet)
    assert telemetry["RotorRPM"] == '95'


def test_calculate_rotor_rpm_is_correct_for_mi8(receiver):
    telemetry = {
        "module": "Mi-8",
        "rotor_rpm_percent": 95.0
    }
    rpm = receiver.calculate_rotor_rpm(telemetry)
    assert int(rpm) == 191


def test_calculate_rotor_rpm_is_correct_for_huey(receiver):
    telemetry = {
        "module": "UH-1H",
        "rotor_rpm_percent": 90.0
    }
    rpm = receiver.calculate_rotor_rpm(telemetry)
    assert int(rpm) == 324

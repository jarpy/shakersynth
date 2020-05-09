from shakersynth.receiver.simshaker import SimShakerReceiver
from pytest import fixture

mi8_packet = """T=35.34;N=Mi-8MT;RotorRPM=95;"""
huey_packet = """T=35.34;N=UH-1H;RotorRPM=90;"""


@fixture
def receiver():
    return SimShakerReceiver(port=None)


def test_parse_returns_rotor_rpm_as_a_string(receiver):
    telemetry = receiver.parse(mi8_packet)
    assert telemetry["RotorRPM"] == '95'

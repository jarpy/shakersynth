from shakersynth.synth.rotor import RotorSynth
from pytest import fixture


@fixture
def rotor():
    return RotorSynth()


def test_calculate_rotor_rpm_is_correct_for_mi8(rotor):
    telemetry = {
        "module": "mi-8",
        "rotor_rpm_percent": 95.0
    }
    rpm = rotor._calculate_rotor_rpm(telemetry)
    assert int(rpm) == 191


def test_calculate_rotor_rpm_is_correct_for_huey(rotor):
    telemetry = {
        "module": "uh-1h",
        "rotor_rpm_percent": 90.0
    }
    rpm = rotor._calculate_rotor_rpm(telemetry)
    assert int(rpm) == 324

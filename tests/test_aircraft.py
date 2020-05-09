import pyo
from shakersynth.aircraft.aircraft import Aircraft
from pytest import fixture


@fixture
def aircraft():
    synth_engine = pyo.Server(audio="offline_nb")
    synth_engine.boot()
    return Aircraft(synth_engine=synth_engine)


def test_get_rotor_rpm_is_correct_for_mi8(aircraft):
    telemetry = {
        "module": "mi-8",
        "rotor_rpm_percent": 95.0
    }
    aircraft.update(telemetry)
    rpm = aircraft.get_rotor_rpm()
    assert int(rpm) == 191


def test_calculate_rotor_rpm_is_correct_for_huey(aircraft):
    telemetry = {
        "module": "uh-1h",
        "rotor_rpm_percent": 90.0
    }
    aircraft.update(telemetry)
    rpm = aircraft.get_rotor_rpm()
    assert int(rpm) == 324

import pyo
from shakersynth.aircraft.aircraft import Aircraft
from shakersynth.synth.rotor import RotorSynth
from pytest import fixture


@fixture
def aircraft():
    synth_engine = pyo.Server(audio="offline_nb")
    synth_engine.boot()
    return Aircraft(synth_engine=synth_engine)


def test_new_aircraft_are_not_running(aircraft):
    assert not aircraft.is_running


def test_aircraft_are_running_after_start(aircraft):
    aircraft.start()
    assert aircraft.is_running


def test_running_aircraft_can_be_stopped(aircraft):
    aircraft.is_running = True
    aircraft.stop()
    assert not aircraft.is_running


def test_aircraft_have_a_rotorsynth(aircraft):
    assert type(aircraft.rotor_synth) is RotorSynth


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


def test_aircraft_data_key_lookup(aircraft):
    aircraft.data = {"food": "jp4"}
    assert aircraft["food"] == "jp4"

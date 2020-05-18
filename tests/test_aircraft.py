from shakersynth.aircraft.aircraft import Aircraft
from shakersynth.synth.rotor import RotorSynth
from pytest import fixture


@fixture
def aircraft():
    return Aircraft()


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
    assert any([type(synth) is RotorSynth
                for synth in aircraft.synths])

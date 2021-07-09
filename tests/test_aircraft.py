from shakersynth.aircraft.aircraft import Aircraft
from shakersynth.synth.rotor import RotorSynth
from pytest import fixture

helicopters = ['mi-8mt', 'mi-24p', 'uh-1h']
fixed_wings = ['a10-c_2']


@fixture
def aircraft():
    def factory(module=None):
        return Aircraft(module)
    return factory


def test_none_type_aircraft_have_no_synths(aircraft):
    assert not aircraft().synths


def test_new_aircraft_are_not_running(aircraft):
    assert not aircraft().is_running


def test_aircraft_are_running_after_start(aircraft):
    ship = aircraft()
    ship.start()
    assert ship.is_running


def test_running_aircraft_can_be_stopped(aircraft):
    ship = aircraft()
    ship.is_running = True
    ship.stop()
    assert not ship.is_running


def test_helicopters_have_a_rotorsynth(aircraft):
    for helicopter in helicopters:
        chopper = aircraft(helicopter)
        assert any(
            [type(synth) is RotorSynth
                for synth in chopper.synths])


def test_fixed_wing_aircraft_do_not_have_a_rotorsynth(aircraft):
    for fixed_wing in fixed_wings:
        plane = aircraft(fixed_wing)
        assert not any(
            [type(synth) is RotorSynth
                for synth in plane.synths])

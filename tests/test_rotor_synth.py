from shakersynth.synth.rotor import RotorSynth
from math import isclose
from pytest import fixture, raises


@fixture
def rotor():
    def factory(module):
        return RotorSynth(module)
    return factory


def test_unsupported_module_raises_exception(rotor):
    with raises(ValueError):
        rotor("whirlybird-5000")


def test_calculate_rotor_rpm_is_correct_for_mi8(rotor):
    rpm = rotor("mi-8mt")._calculate_rotor_rpm(95.0)
    assert isclose(rpm, 200)


def test_calculate_rotor_rpm_is_correct_for_mi24(rotor):
    rpm = rotor("mi-24p")._calculate_rotor_rpm(95.0)
    assert isclose(rpm, 280)


def test_calculate_rotor_rpm_is_correct_for_huey(rotor):
    rpm = rotor("uh-1h")._calculate_rotor_rpm(90.)
    assert isclose(rpm, 324)

from shakersynth.receiver.shakersynth import ShakersynthReceiver
from unittest.mock import Mock
from pytest import fixture
from textwrap import dedent

mi8_payload = dedent(
    """
    ---
    module: Mi-8MT
    rotor_rpm_percent: 95.332
    """
).strip().encode()

mi24_payload = dedent(
    """
    ---
    module: Mi-24P
    rotor_rpm_percent: 95.332
    """
).strip().encode()

huey_payload = dedent(
    """
    ---
    module: UH-1H
    rotor_rpm_percent: 90.167
    """
).strip().encode()


@fixture
def mi8():
    receiver = ShakersynthReceiver()
    receiver._receive_udp = Mock()
    receiver._receive_udp.return_value = mi8_payload
    return receiver.receive()


@fixture
def mi24():
    receiver = ShakersynthReceiver()
    receiver._receive_udp = Mock()
    receiver._receive_udp.return_value = mi24_payload
    return receiver.receive()


@fixture
def huey():
    receiver = ShakersynthReceiver()
    receiver._receive_udp = Mock()
    receiver._receive_udp.return_value = huey_payload
    return receiver.receive()


def test_module_name_lowercase(mi8, mi24, huey):
    assert mi8["module"] == "mi-8mt"
    assert mi24["module"] == "mi-24p"
    assert huey["module"] == "uh-1h"


def test_rotor_rpm_percent_is_a_float(mi8, mi24, huey):
    for chopper in [mi8, mi24, huey]:
        assert type(chopper["rotor_rpm_percent"]) is float

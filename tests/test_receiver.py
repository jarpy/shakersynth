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
)
mi8_payload = mi8_payload.strip().encode()

huey_payload = dedent(
    """
    ---
    module: UH-1H
    rotor_rpm_percent: 90.167
    """
)
huey_payload = huey_payload.strip().encode()


@fixture
def mi8():
    receiver = ShakersynthReceiver()
    receiver._receive_udp = Mock()
    receiver._receive_udp.return_value = mi8_payload
    return receiver.get_telemetry()


@fixture
def huey():
    receiver = ShakersynthReceiver()
    receiver._receive_udp = Mock()
    receiver._receive_udp.return_value = huey_payload
    return receiver.get_telemetry()


def test_module_name_is_short_and_lowercase(mi8, huey):
    assert mi8["module"] == "mi-8"
    assert huey["module"] == "uh-1h"


def test_rotor_rpm_percent_is_a_float(mi8, huey):
    for chopper in [mi8, huey]:
        assert type(chopper["rotor_rpm_percent"]) is float

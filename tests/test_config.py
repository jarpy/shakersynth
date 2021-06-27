from shakersynth.config import config
from textwrap import dedent


def assert_defaults():
    assert type(config.sample_rate) is int
    assert config.sample_rate == 44100

    assert type(config.buffer_size) is int
    assert config.buffer_size == 2048

    assert type(config.global_volume) is float
    assert config.global_volume == 0.90


def test_defaults():
    assert_defaults()


def test_default_yaml_matches_real_defaults():
    config.sample_rate = None
    config.buffer_size = None
    config.global_volume = None
    config.load_yaml(config.default_yaml)
    assert_defaults()


def test_can_set_values_from_yaml():
    yaml = dedent(
        """
        sample_rate: 48000
        buffer_size: 512
        global_volume: 0.66
        """
    ).strip()
    config.load_yaml(yaml)
    assert config.sample_rate == 48000
    assert config.buffer_size == 512
    assert config.global_volume == 0.66


def test_types_are_correctly_cast_from_yaml():
    yaml = dedent(
        """
        global_volume: 1
        """
    ).strip()
    config.load_yaml(yaml)
    assert type(config.global_volume) is float
    assert config.global_volume == 1.0

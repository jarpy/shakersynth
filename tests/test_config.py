from shakersynth.config import loader
from textwrap import dedent

config = loader.load_config()


def assert_defaults():
    assert type(config.audio.sample_rate) is int
    assert config.audio.sample_rate == 44100

    assert type(config.audio.buffer_size) is int
    assert config.audio.buffer_size == 2048

    assert type(config.audio.global_volume) is float
    assert config.audio.global_volume == 0.70


def test_defaults():
    assert_defaults()


def test_types_are_correctly_cast_from_yaml():
    yaml = dedent(
        """
        audio:
          global_volume: 1
        """
    ).strip()
    with open(loader.get_config_file_path(), "w") as cfg_file:
        cfg_file.write(yaml)
    test_config = loader.load_config()
    assert type(test_config.audio.global_volume) is float
    assert test_config.audio.global_volume == 1.0

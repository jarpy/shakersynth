from shakersynth.config import config
from textwrap import dedent


def test_defaults():
    assert config.audio_api == "wasapi"
    assert config.sample_rate == 44100
    assert config.buffer_size == 1024
    assert config.global_volume == 0.90


def test_can_set_values_from_yaml():
    yaml = dedent(
        """
        audio_api: asio
        sample_rate: 48000
        buffer_size: 512
        global_volume: 0.66
        """
    ).strip()
    config.load_yaml(yaml)
    assert config.audio_api == "asio"
    assert config.sample_rate == 48000
    assert config.buffer_size == 512
    assert config.global_volume == 0.66

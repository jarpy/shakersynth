import logging
import os
import platform
import sys
import yaml

from textwrap import dedent

audio_api: str = "wasapi"
sample_rate: int = 44100
buffer_size: int = 2048
global_volume: float = 0.90

log_level = getattr(
    logging,
    os.getenv('SHAKERSYNTH_LOG_LEVEL', 'info').upper()
)

default_yaml = dedent(
    """
    # Be sure to use the sample rate that your sound card expects.
    sample_rate: 44100

    # If you get audio glitches, try increasing the buffer to 4096.
    buffer_size: 2048

    # Set the overall volume between 0 and 1.0.
    #
    # Values above 0.7 can cause clipping distortion (at least on
    # on the author's system).
    global_volume: 0.7
    """
    ).strip()

if platform.system() == 'Windows':
    config_dir = os.path.join(
        os.environ['LOCALAPPDATA'],
        'Shakersynth'
    )
else:
    config_dir = os.path.join(
        os.environ['HOME'],
        '.shakersynth'
    )


def get_config_file_path() -> str:
    default = os.path.join(config_dir, 'shakersynth.yml')
    return os.getenv("SHAKERSYNTH_CONFIG_FILE", default)


def create_default_config_file() -> None:
    config_file_path = get_config_file_path()
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)

    if not os.path.exists(config_file_path):
        with open(config_file_path, 'w') as config_file:
            config_file.write(default_yaml)


def load_yaml(config_yaml: str) -> None:
    config_from_file = yaml.safe_load(config_yaml)
    this_module = sys.modules[__name__]

    for key, value in config_from_file.items():
        if key in ["global_volume"]:
            value = float(value)
        setattr(this_module, key, value)


create_default_config_file()
with open(get_config_file_path()) as config_file:
    load_yaml(config_file.read())

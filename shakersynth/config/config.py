import logging
import os
import platform
import sys
import yaml

from textwrap import dedent

log_level = getattr(
    logging,
    os.getenv('SHAKERSYNTH_LOG_LEVEL', 'info').upper()
)

defaults = {
    "audio_api": "wasapi",
    "sample_rate": 44100,
    "buffer_size": 1024,
    "global_volume": 0.90,
}

default_yaml = dedent(
    """
    # Select and configure the audio API.
    # Options on Windows are "mme", "directsound", "asio", "wasapi", "wdm-ks".
    #
    # See also: http://ajaxsoundstudio.com/pyodoc/winaudioinspect.html
    #
    # WARNING: This option does not currently work. The default API is always
    # used!
    audio_api: wasapi

    sample_rate: 44100
    buffer_size: 1024

    # Set the overall volume between 0 and 1.0.
    global_volume: 0.90
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


def get_default_config_file_path():
    return os.path.join(config_dir, 'shakersynth.yml')


def create_default_config_file():
    config_file_path = get_default_config_file_path()
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)

    if not os.path.exists(config_file_path):
        with open(config_file_path, 'w') as config_file:
            config_file.write(default_yaml)


def load_yaml(config_yaml: str) -> None:
    config_from_file = yaml.safe_load(config_yaml)

    merged_config = defaults.copy()
    merged_config.update(config_from_file)

    # Map all options in the config to attributes of this module.
    # FIXME: This is too clever and breaks static analysis tools like mypy.
    config_module = sys.modules[__name__]
    for key, value in merged_config.items():
        setattr(config_module, key, merged_config[key])


create_default_config_file()
with open(get_default_config_file_path()) as config_file:
    load_yaml(config_file.read())

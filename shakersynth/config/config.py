import logging
import os
import platform
import sys
import yaml

from textwrap import dedent

#try:
log_level = getattr(
    logging,
    os.getenv('SHAKERSYNTH_LOG_LEVEL', 'info').upper()
)
#except KeyError:
#    log_level = logging.INFO

default_yaml = dedent(
    """
    # Select and configure the audio API.
    # Options on Windows are "mme", "directsound", "asio", "wasapi", "wdm-ks".
    #
    # See also: http://ajaxsoundstudio.com/pyodoc/winaudioinspect.html
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
config_file_path = os.path.join(config_dir, 'shakersynth.yml')

if not os.path.exists(config_dir):
    os.mkdir(config_dir)

if not os.path.exists(config_file_path):
    with open(config_file_path, 'w') as config_file:
        config_file.write(default_yaml)

config_yaml = open(config_file_path).read()
config_from_file = yaml.safe_load(config_yaml)

# Map all options in the config file to attributes of this "config" module.
config_module = sys.modules[__name__]
for key, value in config_from_file.items():
    setattr(config_module, key, config_from_file[key])
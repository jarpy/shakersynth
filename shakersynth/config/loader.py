import logging
import os
import platform
from typing import Callable

from config import ConfigurationSet, config_from_env, config_from_yaml
from textwrap import dedent


default_yaml = dedent(
    """
    ---
    # Audio and sound card settings.
    audio:
      # Be sure to use the sample rate that your sound card expects.
      sample_rate: 44100

      # If you get audio glitches, try increasing the buffer to 4096.
      buffer_size: 2048

      # Set the overall volume between 0 and 1.0.
      #
      # Values above 0.7 can cause clipping distortion (at least on
      # on the author's system).
      global_volume: 0.7

    # Logging options.
    log:
      # Set level to "debug" for very verbose logging.
      level: info

    # Configuration of individual modules and effects.
    modules:
      uh-1h:
        effects:
          rotor:
            enabled: true
      mi-24p:
        effects:
          rotor:
            enabled: true
      mi-8mt:
        effects:
          rotor:
            enabled: true
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


def mutate(conf: dict, key: str, func: Callable):
    """Change the value of `conf[key]` by passing it to `func`."""
    conf[key] = func(conf[key])
    return conf


def load_config():
    create_default_config_file()
    with open(get_config_file_path()) as f:
        cfg = ConfigurationSet(
            config_from_env("SHAKERSYNTH", separator="_", lowercase_keys=True),
            config_from_yaml(f.read()),
            config_from_yaml(default_yaml))

    cfg = mutate(cfg, "audio.global_volume", lambda x: float(x))
    cfg = mutate(cfg, "log.level", lambda x: getattr(logging, x.upper()))

    return cfg

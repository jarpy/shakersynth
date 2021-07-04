import config
import pyo
import os

from shakersynth.config.loader import default_yaml, get_config_file_path

# Create a silent pyo server so that we can create audio objects without
# them complaining that there is no server.
synth_engine = pyo.Server(audio="offline_nb")
synth_engine.boot()

# Set up a default config file in a special location so the user's config
# file doesn't upset the tests.
config_file = 'shakersynth_test_config.yaml'
os.environ["SHAKERSYNTH_CONFIG_FILE"] = config_file

with open(config_file, "w") as cfg_file:
    cfg_file.write(default_yaml)

import pyo
import os

# Create a silent pyo server so that we can create audio objects without
# them complaining that there is no server.
synth_engine = pyo.Server(audio="offline_nb")
synth_engine.boot()

config_file = 'shakersynth_test_config.yaml'
if os.path.exists(config_file):
    os.unlink(config_file)
os.environ["SHAKERSYNTH_CONFIG_FILE"] = config_file

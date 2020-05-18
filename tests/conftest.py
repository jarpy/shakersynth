import pyo

# Create a silent pyo server so that we can create audio objects without
# them complaining that there is no server.
synth_engine = pyo.Server(audio="offline_nb")
synth_engine.boot()

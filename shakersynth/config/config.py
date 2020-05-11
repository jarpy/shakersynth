import logging
import os

try:
    log_level = getattr(logging,
                        os.getenv('SHAKERSYNTH_LOG_LEVEL', 'info').upper())
except KeyError:
    log_level_name = logging.INFO

global_volume = 0.7

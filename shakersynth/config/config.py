import logging
import os
import sys

try:
    log_level = getattr(logging,
                        os.getenv('SHAKERSYNTH_LOG_LEVEL', 'info').upper())
except KeyError:
    log_level_name = logging.INFO

global_volume = 0.95

# Only offer to use audio devices that have the following string in their
# API name.
if sys.platform == 'Win32':
    audio_api_filter_string = 'DirectSound'
else:
    audio_api_filter_string = 'Pulse'

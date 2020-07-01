__title__ = 'echome-sdk'
__version__ = '0.1.0'
__author__ = 'Marcus Gutierrez'

import logging
import os
from .session import Session, Vm, Images, SshKey

debug_level = os.getenv("ECHOME_DEBUG", "error")
if debug_level == "error":
    lv = logging.ERROR
elif debug_level == "debug":
    lv = logging.DEBUG
elif debug_level == "info":
    lv = logging.INFO
elif debug_level == "warning":
    lv = logging.WARNING
else:
    raise Exception("Unknown debug level set in ECHOME_DEBUG environment variable.")

logger = logging.getLogger()
# If the logger's level was set outside of this function, use that value instead.
# Otherwise, grab what was set in the environment variable, or fall back to the default.
if logger.level == logging.ERROR:
    logging.basicConfig(level=lv)
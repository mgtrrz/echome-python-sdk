__title__ = 'echome-sdk'
__version__ = '0.3.0'
__author__ = 'Marcus Gutierrez'

import logging
import os
from .session import Session

debug_level = os.getenv("ECHOME_DEBUG", "WARNING")
if debug_level == "ERROR":
    lv = logging.ERROR
elif debug_level == "DEBUG":
    lv = logging.DEBUG
elif debug_level == "INFO":
    lv = logging.INFO
elif debug_level == "WARNING":
    lv = logging.WARNING
else:
    raise Exception("Unknown debug level set in ECHOME_DEBUG environment variable.")

logging.basicConfig(level=lv)

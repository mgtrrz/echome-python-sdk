__title__ = 'echome-sdk'
__version__ = '0.5.0'
__author__ = 'Marcus Gutierrez'

import logging
import os
from .session import Session

LOGLEVEL = os.getenv("ECHOME_DEBUG", "WARNING").upper()
logging.basicConfig(level=LOGLEVEL)

logger = logging.getLogger(__name__)
logger.setLevel(LOGLEVEL)

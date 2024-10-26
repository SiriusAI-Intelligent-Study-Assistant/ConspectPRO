# -*- coding: utf-8 -*-

import logging
import locale

file_log = logging.FileHandler('logs.log')
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out), 
                    format='[%(asctime)s | %(levelname)s]: %(message)s', 
                    datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.INFO)

locale.getpreferredencoding = lambda: "UTF-8"

from .translator import translate
from .note_processing.create_llm_session import CreateLLMSession
from .config import *

__version__ = '0.0.1'
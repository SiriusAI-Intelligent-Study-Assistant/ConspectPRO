"""Free Google Translate API for Python. Translates totally free of charge."""
__all__ = 'Translator',
__version__ = '3.1.0-alpha'


from .client import Translator
from .constants import LANGCODES, LANGUAGES  # noqa

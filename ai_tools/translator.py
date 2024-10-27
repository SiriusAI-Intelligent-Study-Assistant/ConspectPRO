# -*- coding: utf-8 -*-

from .googletrans_httpx import Translator
import logging


def translate(to_lang: str, text: str) -> str:
    '''
    The function uses the “translate” library,
    which accesses a service (mymemory, microsoft, deepl, libre)
    via API to translate a piece of text from one language to another

    Example: translate("en", "Привет, мир!")
    '''

    translator = Translator()
    try:
        translation = translator.translate(text, dest=to_lang).text
        logging.info(f'Translate "{text}" --> "{translation}" from autodetected to <{to_lang}>')
        return translation

    except Exception as e:
        logging.error(repr(e))
        raise

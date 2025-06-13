"""
OCR utilities.
"""

import pytesseract
from langcodes import Language
from PIL.Image import Image

_ALL_LANGUAGES = "eng"  # TODO
"""Combined language tag with all supported languages"""


def _get_language(locale: Language) -> str:
    """
    Obtains the Tesseract language code for a locale.

    :param locale: The locale
    :return: The language code
    """

    match locale.to_tag():
        case "zh-sim":
            return "chi_sim"
        case "zh-tra":
            return "chi_tra"
        case _:
            return locale.to_alpha3()


def extract_text(screenshot: Image, locale: Language | None) -> str:
    """
    Extracts text from a screenshot.

    :param screenshot: The screenshot to extract from
    :param locale: The screenshot locale, if known
    :return: The extracted text
    """

    language = _get_language(locale) if locale else _ALL_LANGUAGES
    text = pytesseract.image_to_string(screenshot, lang=language, timeout=60)
    if not isinstance(text, str):
        raise ValueError("Tesseract did not return a string")

    return text

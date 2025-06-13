"""
OCR utilities.
"""

from collections.abc import Iterable

import pytesseract
from langcodes import Language
from PIL.Image import Image


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


def _make_language_string(locales: Iterable[Language]) -> str:
    """
    Constructs the Tesseract language string for a set of locales.

    :param locales: The locales to specify
    :return: The language string
    """

    return "+".join({_get_language(locale) for locale in locales})


_ALL_LANGUAGES = _make_language_string(
    Language.get(locale)
    for locale in ("en-US",)  # TODO
)
"""Combined language tag with all supported languages"""


def extract_text(screenshot: Image, locales: Iterable[Language] | None) -> str:
    """
    Extracts text from a screenshot.

    :param screenshot: The screenshot to extract from
    :param locales: The possible screenshot locales, if known
    :return: The extracted text
    """

    text = pytesseract.image_to_string(
        image=screenshot,
        lang=_make_language_string(locales) if locales else _ALL_LANGUAGES,
        timeout=60,
    )
    if not isinstance(text, str):
        raise ValueError("Tesseract did not return a string")

    return text

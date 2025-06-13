"""
OCR utilities.
"""

from langcodes import Language
from PIL.Image import Image


def extract_text(screenshot: Image, locale: Language | None) -> str:
    """
    Extracts text from a screenshot.

    :param screenshot: The screenshot to extract from
    :param locale: The screenshot locale, if known
    :return: The extracted text
    """

    return ""  # TODO

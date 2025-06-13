"""
Parsing of text extracted from a screenshot.
"""

from collections.abc import Iterable
from datetime import date

from langcodes import Language
from pydantic import BaseModel, ConfigDict


class ScreenshotData(BaseModel):
    """
    Data contained in a screenshot.
    """

    model_config = ConfigDict(frozen=True)

    next_billing_date: date
    """The next billing date"""


def parse_extracted_text(
    extracted_text: str, locales: Iterable[Language] | None
) -> ScreenshotData | None:
    """
    Parses text extracted from a screenshot.

    :param extracted_text: The text extracted from the screenshot
    :param locales: The possible screenshot locales, if known
    :return: The parsed data, or `None` if it could not be parsed
    """

    return ScreenshotData(next_billing_date=date(2025, 1, 1))  # TODO

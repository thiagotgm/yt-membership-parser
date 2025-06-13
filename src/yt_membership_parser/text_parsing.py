"""
Parsing of text extracted from a screenshot.
"""

import logging
from collections.abc import Iterable
from datetime import date, datetime

import dateparser
from dateutil.relativedelta import relativedelta
from langcodes import Language
from pydantic import BaseModel, ConfigDict

from .locales import PARSER_MAP, SUPPORTED_LOCALES

_LOGGER = logging.getLogger(__name__)


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

    if locales is None:
        locales = SUPPORTED_LOCALES

    for locale in locales:
        parser = PARSER_MAP[locale]

        billing_match = parser.billing_pattern.search(extracted_text)
        if not billing_match:
            continue

        _LOGGER.debug("Matched locale %s", locale)

        billing: str = billing_match.group("billing")
        if not billing:
            raise ValueError("Billing group not found, pattern might be incorrect")
        billing = parser.billing_post_processor(billing)
        date.strftime

        renewal_date = dateparser.parse(
            date_string=billing,
            locales=(parser.dateparser_locale,),
            settings={
                "PREFER_DATES_FROM": "past",
                # Add an extra day as a buffer for timezones
                "RELATIVE_BASE": datetime.now() + relativedelta(months=1, days=1),
            },
        )

        if not renewal_date:
            _LOGGER.warning("Matched format for %s but invalid date: '%s'", locale, billing)
            return None

        return ScreenshotData(
            next_billing_date=renewal_date.date(),
        )

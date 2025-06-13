"""
Definitions of supported locales.
"""

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

from langcodes import Language
from langcodes.tag_parser import LanguageTagError


def parse_locale(locale_str: str) -> Language | None:
    """
    Parses a locale.

    :param locale_str: The locale string
    :return: The parsed locale, or `None` if the given string is not a valid locale
    """

    try:
        locale = Language.get(locale_str)
    except LanguageTagError:
        return None

    if not locale.is_valid():
        return None

    if not locale.language:
        return None

    return locale


@dataclass(frozen=True)
class LocaleParserSpec:
    """
    Specification for parsing a supported locale.
    """

    locale: Language
    """The locale code"""

    dateparser_locale: str
    """The locale code to use with dateparser"""

    billing_pattern: re.Pattern
    """The pattern that matches the billing line"""

    billing_post_processor: Callable[[str], str]
    """Post-processor function to apply to matched billing line"""

    @classmethod
    def of(
        cls,
        *,
        locale: str,
        dateparser_locale: str | None = None,
        billing_pattern: str,
        billing_post_processor: Callable[[str], str] = lambda b: b,
    ) -> Self:
        """
        Creates a new instance.

        :param locale: The locale code
        :param dateparser_locale: The locale code to use with dateparser, if different than the
                                  main locale code
        :param billing_pattern: The pattern that matches the billing line
        :param billing_post_processor: Post-processor function to apply to matched billing line
        """

        locale_obj = parse_locale(locale)
        if not locale_obj:
            raise ValueError(f"Invalid locale {locale}")

        return cls(
            locale=locale_obj,
            dateparser_locale=dateparser_locale or locale_obj.to_tag(),
            billing_pattern=re.compile(billing_pattern),
            billing_post_processor=billing_post_processor,
        )


PARSERS: tuple[LocaleParserSpec, ...] = (
    LocaleParserSpec.of(
        locale="en-US",
        dateparser_locale="en",
        billing_pattern=r"Next billing date: (?P<billing>\w++ \d++)",
    ),
)
"""The available parsers"""

PARSER_MAP: dict[Language, LocaleParserSpec] = {parser.locale: parser for parser in PARSERS}
"""The parsers, keyed by the locale"""

SUPPORTED_LOCALES: frozenset[Language] = frozenset(parser.locale for parser in PARSERS)
"""The supported locales"""

if len(PARSERS) > len(SUPPORTED_LOCALES):
    raise ValueError("Duplicate parser detected")  # Sanity check


def find_matching_locales(locale: Language) -> tuple[Language, ...]:
    """
    Obtains the supported locales that match a requested locale.

    :param locale: The requested locale
    :return: The matching supported locales
    """

    locale_tag = locale.to_tag()
    matches = {
        loc
        for loc in SUPPORTED_LOCALES
        if loc == locale or loc.to_tag().startswith(f"{locale_tag}-")
    }
    if matches:
        return tuple(matches)

    matches = {loc for loc in SUPPORTED_LOCALES if locale_tag.startswith(f"{loc.to_tag()}-")}
    return tuple(matches)

"""
Tests for the `locales` module.
"""

from langcodes import Language

from yt_membership_parser.api import find_matching_locales


def test_find_matching_locales():
    assert find_matching_locales(Language.get("en-US")) == (Language.get("en-US"),)
    assert find_matching_locales(Language.get("en")) == (Language.get("en-US"),)

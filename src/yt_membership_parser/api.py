"""
API definition.
"""

import logging
from io import BytesIO
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Request, status
from langcodes import Language
from PIL import Image
from pydantic import BaseModel, ConfigDict

from .image_processing import process_screenshot
from .locales import parse_locale
from .ocr import extract_text
from .text_parsing import ScreenshotData, parse_extracted_text

app = FastAPI(
    title="YouTube Membership Parser",
    description="API for parsing YouTube membership billing screenshots",
    version="0.1.0",
)

_LOGGER = logging.getLogger(__name__)


class ParseResult(BaseModel):
    """
    The result of a screenshot parse operation.
    """

    model_config = ConfigDict(frozen=True)

    parsed_data: ScreenshotData | None
    """The data parsed from the screenshot"""


def _find_matching_locales(locale: Language) -> tuple[Language, ...]:
    """
    Obtains the supported locales that match a requested locale.

    :param locale: The requested locale
    :return: The matching supported locales
    """

    return (locale,)  # TODO


@app.post(
    "/parse",
    openapi_extra={
        "requestBody": {
            "content": {
                "image/*": {
                    "schema": {
                        "type": "string",
                        "format": "binary",
                    },
                },
            },
        },
    },
)
async def parse_screenshot(
    request: Request,
    locale: Annotated[
        str | None,
        Query(
            description="The locale to parse as, if known",
        ),
    ] = None,
) -> ParseResult:
    """
    Parses a membership screenshot.
    """

    if locale is not None:
        requested_locale = parse_locale(locale)
        if not requested_locale:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid locale {locale}"
            )

        locales = _find_matching_locales(requested_locale)
        if not locales:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Locale not supported {locale}"
            )
    else:
        locales = None

    # Only read image data once all other inputs have been validated to avoid wasting badwidth
    screenshot_data = BytesIO()
    async for chunk in request.stream():
        screenshot_data.write(chunk)
    screenshot = Image.open(screenshot_data)

    processed_screenshot = process_screenshot(screenshot=screenshot)
    extracted_text = extract_text(screenshot=processed_screenshot, locales=locales)
    _LOGGER.debug("Extracted text: %s", extracted_text)
    parsed = parse_extracted_text(extracted_text=extracted_text, locales=locales)

    return ParseResult(parsed_data=parsed)

"""
Image processing.
"""

from PIL import ImageEnhance, ImageOps
from PIL.Image import Image, Resampling

_SCALE_FACTOR = 1.6
_SHARPENING_FACTOR = 3


def process_screenshot(screenshot: Image) -> Image:
    """
    Processes a screenshot for OCR usage.

    :param screenshot: The screenshot to process
    :return: The processed screenshot
    """

    screenshot = ImageOps.grayscale(screenshot)
    screenshot = screenshot.resize(
        size=(
            int(screenshot.size[0] * _SCALE_FACTOR),
            int(screenshot.size[1] * _SCALE_FACTOR),
        ),
        resample=Resampling.BILINEAR,
    )
    screenshot = ImageEnhance.Sharpness(screenshot).enhance(_SHARPENING_FACTOR)
    screenshot = screenshot.convert("RGB")

    return screenshot

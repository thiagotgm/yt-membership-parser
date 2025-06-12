"""
API definition.
"""

from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

app = FastAPI(
    title="YouTube Membership Parser",
    description="API for parsing YouTube membership billing screenshots",
    version="0.1.0",
)


class ParseResult(BaseModel):
    """
    The result of a screenshot parse operation.
    """

    model_config = ConfigDict(frozen=True)

    next_billing_date: date


@app.get("/parse")
async def parse_screenshot() -> ParseResult:
    """
    Parses a membership screenshot.
    """

    return ParseResult(next_billing_date=date(2025, 1, 1))

"""
API definition.
"""

from fastapi import FastAPI

app = FastAPI(
    title="YouTube Membership Parser",
    description="API for parsing YouTube membership billing screenshots",
    version="0.1.0",
)


@app.get("/parse")
async def parse_screenshot():
    """
    Parses a membership screenshot.
    """
    raise NotImplementedError()

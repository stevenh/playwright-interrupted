import logging

import pytest
from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)
from playwright.async_api import Error as PlaywrightError

_LOGGER = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_playwright() -> None:
    playwright: Playwright = await async_playwright().start()
    browser: Browser = await playwright.chromium.launch()
    context: BrowserContext = await browser.new_context()
    page: Page = await context.new_page()

    # Check goto about:blank works.
    await page.goto("about:blank")

    with pytest.raises(PlaywrightError):
        await page.goto("http://localhost:7890")  # This should be an unreachable port.

    # This should work without any issues but fails with:
    # Page.goto: Navigation to "about:blank" is interrupted by another navigation to "chrome-error://chromewebdata/"
    await page.goto("about:blank")

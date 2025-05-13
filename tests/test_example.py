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
    logging.basicConfig(level=logging.INFO)

    playwright: Playwright = await async_playwright().start()
    browser: Browser = await playwright.chromium.launch()
    context: BrowserContext = await browser.new_context()
    page: Page = await context.new_page()

    # Check goto about:blank works.
    _LOGGER.info("goto about:blank")
    await page.goto("about:blank")
    _LOGGER.info("goto about:blank succeeded")

    with pytest.raises(PlaywrightError):
        _LOGGER.info("goto invalid url (unreachable port)")
        await page.goto("http://localhost:7890")  # This should be an unreachable port.

    # This should work without any issues first time but fails with:
    # Page.goto: Navigation to "about:blank" is interrupted by another navigation to "chrome-error://chromewebdata/"
    _LOGGER.info("goto about:blank again")
    failures: int = 0
    for i in range(5):
        i += 1
        try:
            await page.goto("about:blank")
        except PlaywrightError as e:
            _LOGGER.error("attempt %d error: %s", i, e)
            failures += 1
        else:
            _LOGGER.info("attempt %d success", i)

    assert failures == 0, f"Page.goto failed {failures} times, expected 0"

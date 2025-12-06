"""
This provides browser and page fixutres.
"""

import pytest
from playwright.sync_api import  sync_playwright

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        page.pause()
        # page.close()
        # browser.close()
        
"""@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def playwright_instance():
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()
"""
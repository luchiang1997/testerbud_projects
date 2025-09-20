import pytest, re
from playwright.sync_api import sync_playwright, Page, expect

# -------- Fixture: Page --------
@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        yield page
        browser.close()

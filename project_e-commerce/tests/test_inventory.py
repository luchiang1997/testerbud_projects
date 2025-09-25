import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def ecommerce_page_elements(page: Page):
    page.goto("https://testerbud.com/practice-ecommerece-website")
    return page

# search specific item
def test_seacrh_function(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    page.get_by_role("searchbox", name="Search").fill("Coca Cola 250ml")
    expect(page.get_by_role("heading", name="Search Results for \"Coca Cola 250ml\"")).to_be_visible()
    expect(page.get_by_text("Coca Cola 250ml", exact=True)).to_be_visible()
    
# not exist item will show every item
def test_add_function(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    page.locator("#quantity-2").fill("2")
    page.locator("div:nth-child(2) > .h-100 > .d-flex.flex-column > .mt-auto > .btn").click()
    page.get_by_role("button", name="2").click()
    expect(page.get_by_text("Wireless Mouse - $25 x 2")).to_be_visible()

def test_remove_function(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    test_add_function(page)
    page.get_by_role("button", name="Remove").click()
    expect(page.get_by_text("Your cart is empty.")).to_be_visible()
    
def test_total_price_function(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    page.locator("#quantity-5").fill("10")
    page.locator("div:nth-child(5) > .h-100 > .d-flex.flex-column > .mt-auto > .btn").click()
    page.locator("#quantity-7").fill("2")
    page.locator("div:nth-child(7) > .h-100 > .d-flex.flex-column > .mt-auto > .btn").click()
    page.get_by_role("button", name="12").click()
    page.locator("div").filter(has_text=re.compile(r"^Coca Cola 250ml - \$1 x 2Remove$")).get_by_role("button").click()
    expect(page.get_by_text("Total: $1800")).to_be_visible()
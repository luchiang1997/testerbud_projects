import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def ecommerce_page_elements(page: Page):
    page.goto("https://testerbud.com/practice-ecommerece-website")
    return page

# EC_E2E_01 test_shopping_success
def test_e2e_ecommerce(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    # Shopping page
    page.get_by_text("Wireless Mouse").click()
    page.locator("#quantity-2").fill("2")
    page.locator("div:nth-child(2) > .h-100 > .d-flex.flex-column > .mt-auto > .btn").click()
    page.get_by_role("button", name="2").click()

    # Order page
    expect(page.get_by_text("Wireless Mouse - $25 x")).to_be_visible()
    expect(page.get_by_text("Total: $")).to_be_visible()
    page.get_by_role("button", name="Proceed to Buy").click()
    
    # Shipping page
    page.get_by_role("textbox", name="Full Name:").fill("Lu Chiang")
    
    page.get_by_role("textbox", name="Street Address:").fill("456 alex street")
    page.get_by_role("textbox", name="City:").fill("Brisbane")
    page.get_by_role("textbox", name="State:").fill("QLD")
    page.get_by_role("textbox", name="ZIP Code:").fill("4000")
    page.get_by_role("button", name="Save Address & Continue to").click()
    
    # Card info
    page.get_by_role("textbox", name="Card Number:").fill("5217 9999 9999")
    page.get_by_role("textbox", name="Expiry Date:").fill("03/29")
    page.get_by_role("textbox", name="CVV:").fill("123")
    page.get_by_role("button", name="Buy Now").click()
    
    # Successful page
    expect(page.get_by_role("heading", name="Order Successful!")).to_be_visible()
    expect(page.get_by_text("Wireless Mouse - $25 x"))
    page.get_by_role("button", name="Done")
    
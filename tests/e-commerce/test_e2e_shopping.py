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
    product_name = "Wireless Mouse"
    quantity = "2"
    full_name = "Lu Chiang"
    address = "456 alex street"
    city = "Brisbane"
    state = "QLD"
    zip_code = "4000"
    card_number = "5217 9999 9999"
    expiry_date = "03/29"
    cvv = "123"

    # Shopping page
    page.get_by_text(product_name).click()
    page.locator("#quantity-2").fill(quantity)
    page.locator("div:nth-child(2) > .h-100 > .d-flex.flex-column > .mt-auto > .btn").click()
    page.get_by_role("button", name=quantity).click()
    expect(page.get_by_text(f"{product_name} - $25 x")).to_be_visible()

    # Order page
    expect(page.get_by_text("Total: $")).to_be_visible()
    page.get_by_role("button", name="Proceed to Buy").click()

    # Shipping page
    page.get_by_role("textbox", name="Full Name:").fill(full_name)
    page.get_by_role("textbox", name="Street Address:").fill(address)
    page.get_by_role("textbox", name="City:").fill(city)
    page.get_by_role("textbox", name="State:").fill(state)
    page.get_by_role("textbox", name="ZIP Code:").fill(zip_code)
    page.get_by_role("button", name="Save Address & Continue to").click()

    # Card info
    page.get_by_role("textbox", name="Card Number:").fill(card_number)
    page.get_by_role("textbox", name="Expiry Date:").fill(expiry_date)
    page.get_by_role("textbox", name="CVV:").fill(cvv)
    page.get_by_role("button", name="Buy Now").click()

    # Successful page
    expect(page.get_by_role("heading", name="Order Successful!")).to_be_visible()
    expect(page.get_by_text(f"{product_name} - $25 x")).to_be_visible()
    expect(page.get_by_role("button", name="Done")).to_be_visible()

import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def ecommerce_page_elements(page: Page):
    page.goto("https://testerbud.com/practice-ecommerece-website")
    return page

def fill_shipping_info(page: Page, name="Jack", street="Hello Rd", city="Sydney", state="NSW", zip_code="1000"):
    product_name = "External SSD 1TB"
    quantity = "10"
    page.locator("#quantity-5").fill(quantity)
    page.locator("div:nth-child(5) > .h-100 > .d-flex.flex-column > .mt-auto > .btn").click()
    page.get_by_role("button", name=quantity).click()
    expect(page.get_by_text(f"{product_name} - $180 x")).to_be_visible()
    page.get_by_role("button", name="Proceed to Buy").click()
    page.get_by_role("textbox", name="Full Name:").fill(name)
    page.get_by_role("textbox", name="Street Address:").fill(street)
    page.get_by_role("textbox", name="City:").fill(city)
    page.get_by_role("textbox", name="State:").fill(state)
    page.get_by_role("textbox", name="ZIP Code:").fill(zip_code)
    page.get_by_role("button", name="Save Address & Continue to").click()

def test_valid_card_fields(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    card_number = "5127 1888 8888 0009"
    expiry_date = "01/29"
    cvv = "008"
    fill_shipping_info(page)
    page.get_by_role("textbox", name="Card Number:").fill(card_number)
    page.get_by_role("textbox", name="Expiry Date:").fill(expiry_date)
    page.get_by_role("textbox", name="CVV:").fill(cvv)
    page.get_by_role("button", name="Buy Now").click()
    expect(page.get_by_role("heading", name="Order Successful!")).to_be_visible()
    expect(page.get_by_text("External SSD 1TB - $180 x 10")).to_be_visible()
    expect(page.get_by_role("button", name="Done")).to_be_visible()

def test_invalid_cards_fields(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    fill_shipping_info(page)
    page.get_by_role("button", name="Buy Now").click()
    expect(page.get_by_text("Please enter card number.")).to_be_visible()
    expect(page.get_by_text("Please enter expiry date.")).to_be_visible()
    expect(page.get_by_text("Please enter CVV.")).to_be_visible()

def test_save_cards_info(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    card_number = "5127 1888 8888 0009"
    expiry_date = "01/29"
    cvv = "008"
    fill_shipping_info(page)
    page.get_by_role("textbox", name="Card Number:").fill(card_number)
    page.get_by_role("textbox", name="Expiry Date:").fill(expiry_date)
    page.get_by_role("textbox", name="CVV:").fill(cvv)
    page.locator("div:has-text('Payment Details') button.btn-close").first.click()
    page.get_by_role("button", name="10").click()
    page.get_by_role("button", name="Proceed to Buy").click()
    page.get_by_role("button", name="Save Address & Continue to").click()
    expect(page.get_by_role("textbox", name="Card Number:")).to_have_value(card_number)
    expect(page.get_by_role("textbox", name="Expiry Date:")).to_have_value(expiry_date)
    expect(page.get_by_role("textbox", name="CVV:")).to_have_value(cvv)


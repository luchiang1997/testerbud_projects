import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def ecommerce_page_elements(page: Page):
    page.goto("https://testerbud.com/practice-ecommerece-website")
    return page

def add_product_to_cart(page: Page, quantity="10"):
    page.locator("#quantity-5").fill(quantity)
    page.locator("div:nth-child(5) > .h-100 > .d-flex.flex-column > .mt-auto > .btn").click()
    page.get_by_role("button", name=quantity).click()
    page.get_by_role("button", name="Proceed to Buy").click()

def fill_shipping_info(page: Page, name, street, city, state, zip_code):
    page.get_by_role("textbox", name="Full Name:").fill(name)
    page.get_by_role("textbox", name="Street Address:").fill(street)
    page.get_by_role("textbox", name="City:").fill(city)
    page.get_by_role("textbox", name="State:").fill(state)
    page.get_by_role("textbox", name="ZIP Code:").fill(zip_code)
    page.get_by_role("button", name="Save Address & Continue to").click()


def test_valid_shipping_fields(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    add_product_to_cart(page)
    fill_shipping_info(page, "Jack", "Hello Rd", "Sydney", "NSW", "1000")
    expect(page.get_by_text("Payment Details")).to_be_visible()
    
def test_save_shipping_info(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    add_product_to_cart(page)
    fill_shipping_info(page, "Jack", "Hello Rd", "Sydney", "NSW", "1000")
    page.locator("div:has-text('Payment Details') button.btn-close").first.click()
    page.get_by_role("button", name="10").click()
    page.get_by_role("button", name="Proceed to Buy").click()
    expect(page.get_by_role("textbox", name="Full Name:")).to_have_value("Jack")
    expect(page.get_by_role("textbox", name="Street Address:")).to_have_value("Hello Rd")
    expect(page.get_by_role("textbox", name="City:")).to_have_value("Sydney")
    expect(page.get_by_role("textbox", name="State:")).to_have_value("NSW")
    expect(page.get_by_role("textbox", name="ZIP Code:")).to_have_value("1000")

def test_invalid_shipping_fields(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    add_product_to_cart(page)
    page.get_by_role("button", name="Save Address & Continue to").click()

    def handle_dialog(dialog):
        assert dialog.message == "Please fill in all address fields."
        dialog.accept()
    page.on("dialog", handle_dialog)
    page.get_by_role("button", name="Save Address & Continue to").click()


import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def ecommerce_page_elements(page: Page):
    page.goto("https://testerbud.com/practice-ecommerece-website")
    return page

def test_seacrh_function(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    search_item = "Coca Cola 250ml"
    page.get_by_role("searchbox", name="Search").fill(search_item)
    expect(page.get_by_role("heading", name=f'Search Results for "{search_item}"')).to_be_visible()
    expect(page.get_by_text(search_item, exact=True)).to_be_visible()
    
def test_add_function(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    product_name = "Wireless Mouse"
    quantity = "2"
    price = "$25"
    page.locator("#quantity-2").fill(quantity)
    page.locator("div:nth-child(2) > .h-100 > .d-flex.flex-column > .mt-auto > .btn").click()
    page.get_by_role("button", name=quantity).click()
    expect(page.get_by_text(f"{product_name} - {price} x {quantity}")).to_be_visible()

def test_remove_function(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    product_name = "Wireless Mouse"
    quantity = "2"
    price = "$25"
    # Add item first
    page.locator("#quantity-2").fill(quantity)
    page.locator("div:nth-child(2) > .h-100 > .d-flex.flex-column > .mt-auto > .btn").click()
    page.get_by_role("button", name=quantity).click()
    expect(page.get_by_text(f"{product_name} - {price} x {quantity}")).to_be_visible()
    # Remove item
    page.get_by_role("button", name="Remove").click()
    expect(page.get_by_text("Your cart is empty.")).to_be_visible()
    
def test_total_price_function(ecommerce_page_elements) -> None:
    page = ecommerce_page_elements
    product1_name = "External SSD 1TB"
    product1_quantity = "10"
    product1_price = "$180"
    product2_name = "Coca Cola 250ml"
    product2_quantity = "2"
    product2_price = "$1"
    total_price = "$1800"
    # Add External SSD 1TB
    page.locator("#quantity-5").fill(product1_quantity)
    page.locator("div:nth-child(5) > .h-100 > .d-flex.flex-column > .mt-auto > .btn").click()
    # Add Coca Cola 250ml
    page.locator("#quantity-7").fill(product2_quantity)
    page.locator("div:nth-child(7) > .h-100 > .d-flex.flex-column > .mt-auto > .btn").click()
    page.get_by_role("button", name=str(int(product1_quantity) + int(product2_quantity))).click()
    page.locator("div").filter(has_text=re.compile(r"^Coca Cola 250ml - \$1 x 2Remove$")).get_by_role("button").click()
    expect(page.get_by_text(f"Total: {total_price}")).to_be_visible()
   






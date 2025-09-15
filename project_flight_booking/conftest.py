import pytest
from playwright.sync_api import sync_playwright, Page, expect

# -------- Fixture: Page --------
@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        yield page
        browser.close()

# -------- Fixture: Flight Search Elements --------
@pytest.fixture
def flight_search_elements(page: Page):
    page.goto("https://testerbud.com/flight-booking-scenarios")
    
    elements = {
        "page": page,
        "from_city": page.get_by_label("From:"),
        "to_city": page.get_by_label("To:"),
        "departure_date": page.get_by_role("textbox", name="Departure Date:"),
        "return_date": page.get_by_role("textbox", name="Return Date:"),
        "passengers": page.get_by_role("spinbutton", name="Passengers:"),
        "travel_class": page.get_by_label("Travel Class:"),
        "one_way_checkbox": page.get_by_role("checkbox", name="One Way"),
        "search_flight_button": page.get_by_role("button", name="Search Flights")
    }
    return elements

# -------- Fixture: Flight Payment Elements --------
@pytest.fixture
def flight_payment_elements(flight_search_elements):
    page = flight_search_elements["page"]
    
    elements = {
        "page": page,
        "card_number": page.get_by_role("textbox", name="Card Number:"),
        "expiry_date": page.get_by_role("textbox", name="Expiry Date:"),
        "cvv": page.get_by_role("textbox", name="CVV:"),
        "book_flight_button": page.get_by_role("button", name="Book Flight")
    }
    return elements

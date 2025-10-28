from playwright.sync_api import expect

# --- Test Data Variables ---
FROM_CITY = "New York"
TO_CITY = "London"
DEPARTURE_DATE = "2026-10-10"
RETURN_DATE = "2026-10-20"
PASSENGERS = "2"
TRAVEL_CLASS = "Economy"
DEPARTURE_FLIGHT = "Global Wings (GW205) -"
RETURN_FLIGHT = "Air Swift (AS790) -"
ERROR_PAYMENT_BLANK = "Please select both departure and return flights and enter complete payment details."

def search_flights(search_elements):
    search_elements["from_city"].select_option(FROM_CITY)
    search_elements["to_city"].select_option(TO_CITY)
    search_elements["departure_date"].fill(DEPARTURE_DATE)
    search_elements["return_date"].fill(RETURN_DATE)
    search_elements["passengers"].fill(PASSENGERS)
    search_elements["travel_class"].select_option(TRAVEL_CLASS)
    search_elements["search_flight_button"].click()
    search_elements["page"].get_by_role("button", name=DEPARTURE_FLIGHT).click()
    search_elements["page"].get_by_role("button", name=RETURN_FLIGHT).click()

# TC_PAY_01 payment details correspond correctly to the selected flights
def test_payment_details_match(flight_search_elements):
    search_elements = flight_search_elements
    page = search_elements["page"]

    search_flights(search_elements)
    expect(page.get_by_text("Global Wings (GW205): New York to London")).to_be_visible()
    expect(page.get_by_text("Departure: 10/10/2026")).to_be_visible()
    expect(page.get_by_text("Air Swift (AS790): London to New York")).to_be_visible()
    expect(page.get_by_text("Departure: 10/20/2026")).to_be_visible()

# TC_PAY_02 cancel payment go back to search flights
def test_payment_cancel(flight_search_elements):
    search_elements = flight_search_elements
    page = search_elements["page"]

    search_flights(search_elements)
    page.get_by_role("button", name="Close").click()
    expect(page.get_by_text("Available Flights")).to_be_visible()

# TC_PAY_03 test the payment info blank and show error msg
def test_payment_info_blank(flight_search_elements):
    search_elements = flight_search_elements
    page = search_elements["page"]

    def handle_dialog(dialog):
        assert dialog.message == ERROR_PAYMENT_BLANK
        dialog.accept()
    page.on("dialog", handle_dialog)

    search_flights(search_elements)
    page.get_by_role("button", name="Book Flight").click()

from playwright.sync_api import expect

# --- Test Data Variables ---
FROM_CITY = "New York"
TO_CITY = "London"
DEPARTURE_DATE = "2026-09-20"
RETURN_DATE = "2026-09-26"
PASSENGERS = "2"
TRAVEL_CLASS = "Economy"
CARD_NUMBER = "571129170711699"
EXPIRY_DATE = "01/27"
CVV = "966"
FLIGHT_NAME = "Sky High Airlines (SH412) -"

def search_flight(search_elements, one_way=True):
    search_elements["from_city"].select_option(FROM_CITY)
    search_elements["to_city"].select_option(TO_CITY)
    search_elements["departure_date"].fill(DEPARTURE_DATE)
    search_elements["passengers"].fill(PASSENGERS)
    search_elements["travel_class"].select_option(TRAVEL_CLASS)
    if not one_way:
        search_elements["return_date"].fill(RETURN_DATE)
    search_elements["one_way_checkbox"].check()
    search_elements["search_flight_button"].click()

def fill_payment(payment_elements):
    payment_elements["card_number"].fill(CARD_NUMBER)
    payment_elements["expiry_date"].fill(EXPIRY_DATE)
    payment_elements["cvv"].fill(CVV)
    payment_elements["book_flight_button"].click()

# TC_E2E_01 test_one_way_flight_booking_success
def test_search_one_way(flight_search_elements, flight_payment_elements):
    page = flight_search_elements["page"]
    search_flight(flight_search_elements, one_way=True)
    expect(page.get_by_role("button", name=FLIGHT_NAME)).to_be_visible()
    page.get_by_role("button", name=FLIGHT_NAME).click()
    fill_payment(flight_payment_elements)
    expect(page.get_by_role("heading", name="Booking Successful!")).to_be_visible()

# TC_E2E_02 test_round_trip_flight_booking_success
def test_search_round_trip(flight_search_elements, flight_payment_elements):
    page = flight_search_elements["page"]
    search_flight(flight_search_elements, one_way=False)
    expect(page.get_by_role("button", name=FLIGHT_NAME)).to_be_visible()
    page.get_by_role("button", name=FLIGHT_NAME).click()
    fill_payment(flight_payment_elements)
    expect(page.get_by_role("heading", name="Booking Successful!")).to_be_visible()



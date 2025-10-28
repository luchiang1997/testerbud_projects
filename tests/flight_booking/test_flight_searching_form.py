from playwright.sync_api import expect

# --- Test Data Variables ---
FROM_CITY = "New York"
TO_CITY = "London"
DEPARTURE_DATE = "2025-09-13"
RETURN_DATE = "2025-09-20"
PAST_RETURN_DATE = "2025-09-10"
FUTURE_DEPARTURE_DATE = "2026-10-01"
PASSENGERS_VALID = "2"
PASSENGERS_INVALID = "0"
TRAVEL_CLASS = "Economy"

ERROR_DEPARTURE_PAST = "Departure date cannot be in the past."
ERROR_RETURN_BEFORE_DEPARTURE = "Return date must be after departure date."
ERROR_PASSENGERS_MIN = "Passengers must be at least 1."
ERROR_SAME_CITY = "Departure and destination cities cannot be the same."

def fill_search_form(search_elements, from_city, to_city, departure_date, return_date=None, passengers="1", travel_class=TRAVEL_CLASS, one_way=False):
    search_elements["from_city"].select_option(from_city)
    search_elements["to_city"].select_option(to_city)
    search_elements["departure_date"].fill(departure_date)
    search_elements["passengers"].fill(passengers)
    search_elements["travel_class"].select_option(travel_class)
    if one_way:
        search_elements["one_way_checkbox"].check()
    elif return_date:
        search_elements["return_date"].fill(return_date)
    search_elements["search_flight_button"].click()

# TC_FIELDS_01 test_invalid_return_dates
def test_invalide_return_dates(flight_search_elements, flight_payment_elements):
    page = flight_search_elements["page"]
    fill_search_form(
        flight_search_elements,
        FROM_CITY,
        TO_CITY,
        DEPARTURE_DATE,
        return_date=PAST_RETURN_DATE,
        passengers=PASSENGERS_VALID
    )
    expect(page.get_by_text(ERROR_DEPARTURE_PAST)).to_be_visible()
    expect(page.get_by_text(ERROR_RETURN_BEFORE_DEPARTURE)).to_be_visible()

# TC_FIELDS_02 test_passengers_exceeding_minimum
def test_invalide_passenger_amount(flight_search_elements, flight_payment_elements):
    page = flight_search_elements["page"]
    fill_search_form(
        flight_search_elements,
        FROM_CITY,
        TO_CITY,
        DEPARTURE_DATE,
        return_date=RETURN_DATE,
        passengers=PASSENGERS_INVALID
    )
    expect(page.get_by_text(ERROR_PASSENGERS_MIN)).to_be_visible()

# TC_FIELDS_03 One-way checkbox disables return date input
def test_disable_return_date(flight_search_elements, flight_payment_elements):
    page = flight_search_elements["page"]
    fill_search_form(
        flight_search_elements,
        FROM_CITY,
        TO_CITY,
        FUTURE_DEPARTURE_DATE,
        passengers="1",
        one_way=True
    )
    expect(flight_search_elements["return_date"]).to_be_hidden()

# TC_FIELDS_04 test_from_to_same_location
def test_from_to_same_location(flight_search_elements, flight_payment_elements):
    page = flight_search_elements["page"]
    fill_search_form(
        flight_search_elements,
        FROM_CITY,
        FROM_CITY,
        FUTURE_DEPARTURE_DATE,
        passengers="1"
    )
    expect(page.get_by_text(ERROR_SAME_CITY)).to_be_visible()







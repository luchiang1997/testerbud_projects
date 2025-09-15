from playwright.sync_api import expect

# TC_SER_01 test_invalid_return_dates
def test_invalide_return_dates(flight_search_elements, flight_payment_elements):
    search_elements = flight_search_elements
    page = search_elements["page"]

    # --- Search Flight ---
    search_elements["from_city"].select_option("New York")
    search_elements["to_city"].select_option("London")
    search_elements["departure_date"].fill("2025-09-13")
    search_elements["return_date"].fill("2025-09-10")
    search_elements["passengers"].fill("2")
    search_elements["travel_class"].select_option("Economy")
    search_elements["search_flight_button"].click()
    
    expect(page.get_by_text("Departure date cannot be in the past.")).to_be_visible()
    expect(page.get_by_text("Return date must be after departure date.")).to_be_visible()
    
    
# TC_SER_02 test_passengers_exceeding_minimum
def test_invalide_passenger_amount(flight_search_elements, flight_payment_elements):
    search_elements = flight_search_elements
    page = search_elements["page"]

    # --- Search Flight ---
    search_elements["from_city"].select_option("New York")
    search_elements["to_city"].select_option("London")
    search_elements["departure_date"].fill("2025-09-13")
    search_elements["return_date"].fill("2025-09-10")
    search_elements["passengers"].fill("0")
    search_elements["travel_class"].select_option("Economy")
    search_elements["search_flight_button"].click()
    
    expect(page.get_by_text("Passengers must be at least 1.")).to_be_visible()
    
    

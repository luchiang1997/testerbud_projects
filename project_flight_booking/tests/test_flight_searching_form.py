from playwright.sync_api import expect

# TC_FIELDS_01 test_invalid_return_dates
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
    
    
# TC_FIELDS_02 test_passengers_exceeding_minimum
def test_invalide_passenger_amount(flight_search_elements, flight_payment_elements):
    search_elements = flight_search_elements
    page = search_elements["page"]

    # --- Search Flight ---
    search_elements["from_city"].select_option("New York")
    search_elements["to_city"].select_option("London")
    search_elements["departure_date"].fill("2025-09-13")
    search_elements["return_date"].fill("2025-09-20")
    search_elements["passengers"].fill("0")
    search_elements["travel_class"].select_option("Economy")
    search_elements["search_flight_button"].click()
    
    expect(page.get_by_text("Passengers must be at least 1.")).to_be_visible()
    
    
# TC_FIELDS_03 One-way checkbox disables return date input
def test_disable_return_date(flight_search_elements, flight_payment_elements):
    search_elements = flight_search_elements
    page = search_elements["page"]

    # --- Search Flight ---
    search_elements["from_city"].select_option("New York")
    search_elements["to_city"].select_option("London")
    search_elements["departure_date"].fill("2026-10-01")
    search_elements["passengers"].fill("1")
    search_elements["travel_class"].select_option("Economy")
    search_elements["one_way_checkbox"].check()
    
    expect((search_elements["return_date"])).to_be_hidden()
    
# TC_FIELDS_04 test_from_to_same_location
def test_from_to_same_location(flight_search_elements, flight_payment_elements):
    search_elements = flight_search_elements
    page = search_elements["page"]
    
    # --- Search Flight ---
    search_elements["from_city"].select_option("New York")
    search_elements["to_city"].select_option("New York")
    search_elements["departure_date"].fill("2026-10-01")
    search_elements["passengers"].fill("1")
    search_elements["travel_class"].select_option("Economy")
    search_elements["search_flight_button"].click()
    
    expect(page.get_by_text("Departure and destination cities cannot be the same.")).to_be_visible()
    
    


    
    

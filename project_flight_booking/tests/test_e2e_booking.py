from playwright.sync_api import expect

# TC_E2E_01 test_one_way_flight_booking_success
def test_search_one_way(flight_search_elements, flight_payment_elements):
    search_elements = flight_search_elements
    page = search_elements["page"]

    # --- Search Flight ---
    search_elements["from_city"].select_option("New York")
    search_elements["to_city"].select_option("London")
    search_elements["departure_date"].fill("2025-09-20")
    search_elements["passengers"].fill("2")
    search_elements["travel_class"].select_option("Economy")
    search_elements["one_way_checkbox"].check()
    search_elements["search_flight_button"].click()
    page.get_by_role("button", name="Sky High Airlines (SH412) -").click()

    # --- Payment ---
    payment_elements = flight_payment_elements
    payment_elements["card_number"].fill("571129170711699")
    payment_elements["expiry_date"].fill("01/27")
    payment_elements["cvv"].fill("966")
    payment_elements["book_flight_button"].click()

    # --- validation ---
    expect(page.get_by_role("heading", name="Booking Successful!")).to_be_visible()

    
# TC_E2E_02 test_round_trip_flight_booking_success
def test_search_round_trip(flight_search_elements, flight_payment_elements):
    search_elements = flight_search_elements
    page = search_elements["page"]

    # --- Search Flight ---
    search_elements["from_city"].select_option("New York")
    search_elements["to_city"].select_option("London")
    search_elements["departure_date"].fill("2025-09-20")
    search_elements["return_date"].fill("2025-09-26")
    search_elements["passengers"].fill("2")
    search_elements["travel_class"].select_option("Economy")
    search_elements["one_way_checkbox"].check()
    search_elements["search_flight_button"].click()
    page.get_by_role("button", name="Sky High Airlines (SH412) -").click()

    # --- Payment ---
    payment_elements = flight_payment_elements
    payment_elements["card_number"].fill("571129170711699")
    payment_elements["expiry_date"].fill("01/27")
    payment_elements["cvv"].fill("966")
    payment_elements["book_flight_button"].click()

    # --- validation ---
    expect(page.get_by_role("heading", name="Booking Successful!")).to_be_visible()
    
    

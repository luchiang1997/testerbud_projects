from playwright.sync_api import expect

# In this test environment, no frontend validation is implemented for payment fields.
# Therefore, this scenario focuses on verifying that the payment details correspond 
# correctly to the selected flights.

# TC_PAY_01 payment details correspond correctly to the selected flights
def test_payment_details_match(flight_search_elements):
    search_elements = flight_search_elements
    page = search_elements["page"]

    # --- Search Flight ---
    search_elements["from_city"].select_option("New York")
    search_elements["to_city"].select_option("London")
    search_elements["departure_date"].fill("2026-10-10")
    search_elements["return_date"].fill("2026-10-20")
    search_elements["passengers"].fill("2")
    search_elements["travel_class"].select_option("Economy")
    search_elements["search_flight_button"].click()
    page.get_by_role("button", name="Global Wings (GW205) -").click()
    page.get_by_role("button", name="Air Swift (AS790) -").click()
    
    expect(page.get_by_text("Global Wings (GW205): New York to London")).to_be_visible()
    expect(page.get_by_text("Departure: 10/10/2026")).to_be_visible()
    expect(page.get_by_text("Air Swift (AS790): London to New York")).to_be_visible()
    expect(page.get_by_text("Departure: 10/20/2026")).to_be_visible()


# TC_PAY_02 cancel payment go back to search flights
def test_payment_cancel(flight_search_elements):
    search_elements = flight_search_elements
    page = search_elements["page"]

    # --- Search Flight ---
    search_elements["from_city"].select_option("New York")
    search_elements["to_city"].select_option("London")
    search_elements["departure_date"].fill("2026-10-10")
    search_elements["return_date"].fill("2026-10-20")
    search_elements["passengers"].fill("2")
    search_elements["travel_class"].select_option("Economy")
    search_elements["search_flight_button"].click()
    page.get_by_role("button", name="Global Wings (GW205) -").click()
    page.get_by_role("button", name="Air Swift (AS790) -").click()
    page.get_by_role("button", name="Close").click()
    
    expect(page.get_by_text("Available Flights")).to_be_visible()
 
 
    
# TC_PAY_03 test the payment info blank and show error msg
def test_payment_info_blank(flight_search_elements):
    search_elements = flight_search_elements
    page = search_elements["page"]

    # --- listen alert ---
    def handle_dialog(dialog):
        assert dialog.message == "Please select both departure and return flights and enter complete payment details."
        dialog.accept()
    page.on("dialog", handle_dialog)

    # --- Search Flight ---
    search_elements["from_city"].select_option("New York")
    search_elements["to_city"].select_option("London")
    search_elements["departure_date"].fill("2026-10-10")
    search_elements["return_date"].fill("2026-10-20")
    search_elements["passengers"].fill("2")
    search_elements["travel_class"].select_option("Economy")
    search_elements["search_flight_button"].click()
    page.get_by_role("button", name="Global Wings (GW205) -").click()
    page.get_by_role("button", name="Air Swift (AS790) -").click()

    # --- Book Flight triggers alert ---
    page.get_by_role("button", name="Book Flight").click()

import re
from playwright.sync_api import Page, expect

# --- Test Data Variables ---
COUNTRY = "Australia"
TITLE = "Ms."
FIRST_NAME = "LU"
LAST_NAME = "CHIANG"
DOB = "1997-08-02"
DATE = "11/09/2025"
EMAIL = "lu@example.com"
PHONE_CODE = "+61"
PHONE_NUMBER = "412345678"
CONTACT_METHOD = "Email"


def fill_web_form(page: Page):
    page.goto("https://testerbud.com/practice-forms")
    page.locator("form div").filter(has_text="Country of ResidenceSelect").get_by_role("combobox").select_option(COUNTRY)
    page.locator("div").filter(has_text=re.compile(r"^TitleSelect TitleMr\.Ms\.Mrs\.Dr\.Prof\.$")).get_by_role("combobox").select_option(TITLE)
    page.locator("div").filter(has_text=re.compile(r"^First Name$")).get_by_role("textbox").fill(FIRST_NAME)
    page.locator("div").filter(has_text=re.compile(r"^Last Name$")).get_by_role("textbox").fill(LAST_NAME)
    page.get_by_role("textbox", name="YYYY-MM-DD").fill(DOB)
    page.get_by_role("textbox", name="dd/mm/yyyy").fill(DATE)
    page.locator("input[type=\"email\"]").fill(EMAIL)
    page.locator("div").filter(has_text=re.compile(r"^Phone Number\+1\+44\+91\+61\+86\+Other$")).get_by_role("combobox").select_option(PHONE_CODE)
    page.locator("input[type=\"tel\"]").fill(PHONE_NUMBER)
    page.locator("div").filter(has_text=re.compile(r"^Email$")).get_by_role("radio").check()


def test_example(page: Page) -> None:
    fill_web_form(page)
    page.get_by_role("button", name="Submit").click()
    expect(page.get_by_text("Details Successfully Added!")).to_be_visible()

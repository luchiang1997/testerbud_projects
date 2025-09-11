import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://testerbud.com/practice-forms")
    page.locator("form div").filter(has_text="Country of ResidenceSelect").get_by_role("combobox").select_option("Australia")
    page.locator("div").filter(has_text=re.compile(r"^TitleSelect TitleMr\.Ms\.Mrs\.Dr\.Prof\.$")).get_by_role("combobox").select_option("Ms.")
    page.locator("div").filter(has_text=re.compile(r"^First Name$")).get_by_role("textbox").fill("LU")
    page.locator("div").filter(has_text=re.compile(r"^Last Name$")).get_by_role("textbox").fill("CHIANG")
    page.get_by_role("textbox", name="YYYY-MM-DD").fill("1997-08-02")
    page.get_by_role("textbox", name="dd/mm/yyyy").fill("11/09/2025")
    page.locator("input[type=\"email\"]").fill("lu@example.com")
    page.locator("div").filter(has_text=re.compile(r"^Phone Number\+1\+44\+91\+61\+86\+Other$")).get_by_role("combobox").select_option("+61")
    page.locator("input[type=\"tel\"]").fill("412345678")
    page.locator("div").filter(has_text=re.compile(r"^Email$")).get_by_role("radio").check()
    page.get_by_role("button", name="Submit").click()
    
    expect(page.get_by_text("Details Successfully Added!")).to_be_visible()

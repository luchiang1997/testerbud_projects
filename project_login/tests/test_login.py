import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def login_page_elements(page: Page):
    page.goto("https://testerbud.com/practice-login-form")
    email_input = page.get_by_label("Email Address")
    password_input = page.get_by_label("Password")
    login_button = page.get_by_role("button", name="Sign in")
    return page, email_input, password_input, login_button

# TC_Basic_01: Verify login with valid credentials
def test_valid_login(login_page_elements) -> None:
    page, email_input, password_input, login_button = login_page_elements
    email_input.fill("user@premiumbank.com")
    password_input.fill("Bank@123")
    login_button.click()
    expect(page.get_by_text("Login Successful!")).to_be_visible()

# TC_Basic_02: Verify login with invalid credentials
def test_invalid_login(login_page_elements) -> None:
    page, email_input, password_input, login_button = login_page_elements
    email_input.fill("user@premiumbank.com")
    password_input.fill("Bank@456")
    login_button.click()
    expect(page.get_by_text("Invalid email id and password")).to_be_visible()

# TC_Basic_03: Check UI elements of the login page    
def test_UI_login(login_page_elements) -> None:
    page, email_input, password_input, login_button = login_page_elements
    expect(page.get_by_text("Email Address")).to_be_visible()
    expect(email_input).to_be_visible()
    expect(page.get_by_text("Password", exact=True)).to_be_visible()
    expect(password_input).to_be_visible()
    expect(page.get_by_text("Remember me")).to_be_visible()
    expect(page.locator("div").filter(has_text=re.compile(r"^Forgot password\?$"))).to_be_visible()
    expect(page.get_by_role("link", name="Register now")).to_be_visible()
    expect(login_button).to_be_visible()

# TC_Basic_04: Verify login button is enable and validate error message when fields are empty    
def test_login_button(login_page_elements) -> None:
    page, email_input, password_input, login_button = login_page_elements
    expect(email_input).to_have_value("")
    expect(password_input).to_have_value("")
    expect(login_button).to_be_enabled()
    login_button.click()
    expect(page.get_by_text("Email and Password are required")).to_be_visible()
    
# TC_Basic_05: Verify password field is masked
def test_login_password_masked(login_page_elements) -> None:
    page, email_input, password_input, login_button = login_page_elements
    expect(password_input).to_have_attribute("type", "password")

# TC_Basic_06: Verify error message when username is entered but password field is left blanked
def test_login_field_empty(login_page_elements) -> None:
    page, email_input, password_input, login_button = login_page_elements
    email_input.fill("user@premiumbank.com")
    expect(password_input).to_have_value("")
    login_button.click()
    expect(page.get_by_text("Password is required")).to_be_visible()
    
# TC_Basic_07: Verify error message when email id entered in invalid format
def test_login_invalid_format(login_page_elements) -> None:
    page, email_input, password_input, login_button = login_page_elements
    email_input.fill("abc123")
    login_button.click()
    expect(email_input).to_have_js_property("validationMessage", "Please include an '@' in the email address. 'abc123' is missing an '@'.")

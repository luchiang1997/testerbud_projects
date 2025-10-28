import re
import pytest
from playwright.sync_api import Page, expect

# --- Test Data Variables ---
EMAIL_VALID = "lu@example.com"
EMAIL_INVALID = "lu123"
PASSWORD_VALID = "!!Bb12345"
PASSWORD_INVALID = "!!Bb123"
PASSWORD_WEAK = "!!B123"
CONFIRM_PASSWORD_VALID = "!!Bb12345"
CONFIRM_PASSWORD_INVALID = "!!Bb123456"

ERROR_EMAIL_REQUIRED = "Email is required"
ERROR_PASSWORD_REQUIRED = "Password is required"
ERROR_CONFIRM_PASSWORD_REQUIRED = "Please confirm your password"
ERROR_EMAIL_FORMAT = "Please include an '@' in the email address. 'lu123' is missing an '@'."
ERROR_PASSWORDS_NOT_MATCH = "Passwords do not match"
SUCCESS_REGISTRATION = "Registration Successful"

# --- Helper Function ---
def fill_registration(page, email, password, confirm_password):
    page.get_by_role("textbox", name="Email Address").fill(email)
    page.get_by_role("textbox", name="Password", exact=True).fill(password)
    page.get_by_role("textbox", name="Confirm Password").fill(confirm_password)
    page.get_by_role("button", name="Register").click()

@pytest.fixture
def register_page_elements(page: Page):
    page.goto("https://testerbud.com/register")
    email_input = page.get_by_role("textbox", name="Email Address")
    password_input = page.get_by_role("textbox", name="Password", exact=True)
    confirm_password_input = page.get_by_role("textbox", name="Confirm Password")
    register_button = page.get_by_role("button", name="Register")
    return page, email_input, password_input, confirm_password_input, register_button

# TC_Registration_01: Verify successful user registration
def test_valid_registration(register_page_elements) -> None:
    page, _, _, _, _ = register_page_elements
    fill_registration(page, EMAIL_VALID, PASSWORD_VALID, CONFIRM_PASSWORD_VALID)
    expect(page.get_by_text(SUCCESS_REGISTRATION)).to_be_visible()
    go_to_login_button = page.get_by_role("button", name="Go to Login")
    expect(go_to_login_button).to_be_visible()

# TC_Registration_02: Verify validation for error message when Email Address left blank
def test_email_blank(register_page_elements) -> None:
    page, email_input, _, _, _ = register_page_elements
    expect(email_input).to_have_value("")
    fill_registration(page, "", PASSWORD_VALID, CONFIRM_PASSWORD_VALID)
    expect(page.get_by_text(ERROR_EMAIL_REQUIRED)).to_be_visible()

# TC_Registration_03: Verify validation for error message when Password left blank
def test_password_blank(register_page_elements) -> None:
    page, _, password_input, _, _ = register_page_elements
    expect(password_input).to_have_value("")
    fill_registration(page, EMAIL_VALID, "", CONFIRM_PASSWORD_VALID)
    expect(page.get_by_text(ERROR_PASSWORD_REQUIRED)).to_be_visible()

# TC_Registration_04: Verify validation for error message when Confirm Password left blank
def test_confirm_password_blank(register_page_elements) -> None:
    page, _, _, confirm_password_input, _ = register_page_elements
    expect(confirm_password_input).to_have_value("")
    fill_registration(page, EMAIL_VALID, PASSWORD_VALID, "")
    expect(page.get_by_text(ERROR_CONFIRM_PASSWORD_REQUIRED)).to_be_visible()

# TC_Registration_05: Verify email validation on registration page
def test_invalid_email(register_page_elements) -> None:
    page, email_input, _, _, _ = register_page_elements
    fill_registration(page, EMAIL_INVALID, PASSWORD_VALID, CONFIRM_PASSWORD_VALID)
    expect(email_input).to_have_js_property("validationMessage", ERROR_EMAIL_FORMAT)

# TC_Registration_06: Verify error message when Password and Confirm Password doesn't match
def test_confirm_password_not_match(register_page_elements) -> None:
    page, _, _, _, _ = register_page_elements
    fill_registration(page, EMAIL_VALID, PASSWORD_VALID, CONFIRM_PASSWORD_INVALID)
    expect(page.get_by_text(ERROR_PASSWORDS_NOT_MATCH)).to_be_visible()

# TC_Registration_07: Validate password strength validation lines colour change
def test_password_validation_colour(register_page_elements) -> None:
    page, _, _, _, _ = register_page_elements
    fill_registration(page, EMAIL_VALID, PASSWORD_INVALID, PASSWORD_INVALID)
    expect(page.get_by_text("At least 8 characters")).to_have_css("color", "rgb(220, 53, 69)")
    expect(page.get_by_text("At least one lowercase letter")).to_have_css("color", "rgb(25, 135, 84)")
    expect(page.get_by_text("At least one uppercase letter")).to_have_css("color", "rgb(25, 135, 84)")
    expect(page.get_by_text("At least one special character")).to_have_css("color", "rgb(25, 135, 84)")
    expect(page.get_by_text("At least one number")).to_have_css("color", "rgb(25, 135, 84)")

# TC_Registration_08: Validate error message when password is weak
def test_password_is_week(register_page_elements) -> None:
    page, _, _, _, _ = register_page_elements
    fill_registration(page, EMAIL_VALID, PASSWORD_WEAK, PASSWORD_INVALID)
    expect(page.get_by_text(ERROR_PASSWORDS_NOT_MATCH)).to_be_visible()

# TC_Registration_09: Verify password strength validation lines colour change to green
def test_password_validation_green(register_page_elements) -> None:
    page, _, _, _, _ = register_page_elements
    
    page.get_by_role("textbox", name="Email Address").fill(EMAIL_VALID)
    page.get_by_role("textbox", name="Password", exact=True).fill(PASSWORD_VALID)
    page.get_by_role("textbox", name="Confirm Password").fill(CONFIRM_PASSWORD_VALID)
    
    expect(page.get_by_text("At least 8 characters")).to_have_css("color", "rgb(25, 135, 84)")
    expect(page.get_by_text("At least one lowercase letter")).to_have_css("color", "rgb(25, 135, 84)")
    expect(page.get_by_text("At least one uppercase letter")).to_have_css("color", "rgb(25, 135, 84)")
    expect(page.get_by_text("At least one special character")).to_have_css("color", "rgb(25, 135, 84)")
    expect(page.get_by_text("At least one number")).to_have_css("color", "rgb(25, 135, 84)")
    
# TC_Registration_10: Validate clicking 'Sign in' link successfully navigate user to Login Page
def test_sign_in_link(register_page_elements) -> None:
    page, _, _, _, _ = register_page_elements
    login_button = page.get_by_role("link", name="Sign in")
    login_button.click()
    expect(page).to_have_url("https://testerbud.com/practice-login-form")

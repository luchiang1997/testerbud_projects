import re
import pytest
from playwright.sync_api import Page, expect

# --- Test Data Variables ---
EMAIL_VALID = "user@premiumbank.com"
EMAIL_INVALID = "user123@premiumbank.com"
SECRET_CODE_VALID = "BANK1234"
SECRET_CODE_INVALID = "BANK12345"
CURRENT_PASSWORD = "Bank@123"
NEW_PASSWORD_VALID = "Bank@12345"
NEW_PASSWORD_INVALID = "1234"
NEW_PASSWORD_MISMATCH = "Brisbane@123456"

ERROR_EMAIL_REQUIRED = "Email is required"
ERROR_EMAIL_NOT_FOUND = "Email not found in our records"
ERROR_SECRET_CODE_REQUIRED = "Secret code is required"
ERROR_SECRET_CODE_INVALID = "Invalid secret code"
ERROR_FIELDS_REQUIRED = "All fields are required"
ERROR_PASSWORDS_NOT_MATCH = "Passwords do not match"
ERROR_PASSWORD_REQUIREMENTS = "Password does not meet requirements"
SUCCESS_PASSWORD_CHANGED = "Password Changed Successfully!"

# --- Helper Functions ---
def fill_email(page, email):
    page.get_by_role("textbox", name="Enter your registered email").fill(email)
    page.get_by_role("button", name="Continue").click()

def fill_secret_code(page, code):
    page.get_by_role("textbox", name="Enter security code").fill(code)
    page.get_by_role("button", name="Verify Code").click()

def fill_passwords(page, current, new, confirm):
    page.get_by_role("textbox", name="Current password").fill(current)
    page.get_by_role("textbox", name="New password", exact=True).fill(new)
    page.get_by_role("textbox", name="Confirm new password").fill(confirm)
    page.get_by_role("button", name="Reset Password").click()

@pytest.fixture
def forget_page_elements(page: Page):
    page.goto("https://testerbud.com/forget-password")
    return page

# TC_Forget_01: Validate Error message if Email address left blank
def test_email_blank(forget_page_elements) -> None:
    page = forget_page_elements
    page.get_by_role("button", name="Continue").click()
    expect(page.get_by_text(ERROR_EMAIL_REQUIRED)).to_be_visible()

# TC_Forget_02: Validate Error message if wrong Email address entered
def test_wrong_email(forget_page_elements) -> None:
    page = forget_page_elements
    fill_email(page, EMAIL_INVALID)
    expect(page.get_by_text(ERROR_EMAIL_NOT_FOUND)).to_be_visible()

# TC_Forget_03: Validate Error message if Secret Code left blank
def test_secret_code_blank(forget_page_elements) -> None:
    page = forget_page_elements
    fill_email(page, EMAIL_VALID)
    expect(page.get_by_role("textbox", name="Enter security code")).to_have_value("")
    page.get_by_role("button", name="Verify Code").click()
    expect(page.get_by_text(ERROR_SECRET_CODE_REQUIRED)).to_be_visible()

# TC_Forget_04: Validate Error message if wrong Secret Code entered
def test_wrong_secret_code(forget_page_elements) -> None:
    page = forget_page_elements
    fill_email(page, EMAIL_VALID)
    fill_secret_code(page, SECRET_CODE_INVALID)
    expect(page.get_by_text(ERROR_SECRET_CODE_INVALID)).to_be_visible()

# TC_Forget_05: Validate Error message if Current Password left blank
def test_current_password_blank(forget_page_elements) -> None:
    page = forget_page_elements
    fill_email(page, EMAIL_VALID)
    fill_secret_code(page, SECRET_CODE_VALID)
    expect(page.get_by_role("textbox", name="Current password")).to_have_value("")
    fill_passwords(page, "", NEW_PASSWORD_VALID, NEW_PASSWORD_VALID)
    expect(page.get_by_text(ERROR_FIELDS_REQUIRED)).to_be_visible()

# TC_Forget_06: Validate Error message if New Password left blank
def test_new_password_blank(forget_page_elements) -> None:
    page = forget_page_elements
    fill_email(page, EMAIL_VALID)
    fill_secret_code(page, SECRET_CODE_VALID)
    page.get_by_role("textbox", name="Current password").fill(CURRENT_PASSWORD)
    expect(page.get_by_role("textbox", name="New password", exact=True)).to_have_value("")
    fill_passwords(page, CURRENT_PASSWORD, "", NEW_PASSWORD_VALID)
    expect(page.get_by_text(ERROR_FIELDS_REQUIRED)).to_be_visible()

# TC_Forget_07: Validate Error message if Confirm New Password left blank
def test_confirm_new_password_blank(forget_page_elements) -> None:
    page = forget_page_elements
    fill_email(page, EMAIL_VALID)
    fill_secret_code(page, SECRET_CODE_VALID)
    page.get_by_role("textbox", name="Current password").fill(CURRENT_PASSWORD)
    page.get_by_role("textbox", name="New password", exact=True).fill(NEW_PASSWORD_VALID)
    expect(page.get_by_role("textbox", name="Confirm new password")).to_have_value("")
    fill_passwords(page, CURRENT_PASSWORD, NEW_PASSWORD_VALID, "")
    expect(page.get_by_text(ERROR_FIELDS_REQUIRED)).to_be_visible()

# TC_Forget_08: Validate error message if New and Confirm Password do not match
def test_confirm_new_old_password_not_match(forget_page_elements) -> None:
    page = forget_page_elements
    fill_email(page, EMAIL_VALID)
    fill_secret_code(page, SECRET_CODE_VALID)
    fill_passwords(page, CURRENT_PASSWORD, NEW_PASSWORD_VALID, NEW_PASSWORD_MISMATCH)
    expect(page.get_by_text(ERROR_PASSWORDS_NOT_MATCH)).to_be_visible()

# TC_Forget_09: Validate error message if New and Confirm Password do not meet password criteria
def test_confirm_new_old_password_not_meet_criteria(forget_page_elements) -> None:
    page = forget_page_elements
    fill_email(page, EMAIL_VALID)
    fill_secret_code(page, SECRET_CODE_VALID)
    fill_passwords(page, CURRENT_PASSWORD, NEW_PASSWORD_INVALID, NEW_PASSWORD_INVALID)
    expect(page.get_by_text(ERROR_PASSWORD_REQUIREMENTS)).to_be_visible()

# TC_Forget_10: Validate password strength indicator when some criteria are met
def test_confirm_new_old_password_are_meet_some_criteria(forget_page_elements) -> None:
    page = forget_page_elements
    fill_email(page, EMAIL_VALID)
    fill_secret_code(page, SECRET_CODE_VALID)
    fill_passwords(page, CURRENT_PASSWORD, "Bb1234", "Bb1234")
    expect(page.get_by_text("Minimum 8 characters")).to_have_css("color", "rgb(220, 53, 69)")
    expect(page.get_by_text("At least one special character")).to_have_css("color", "rgb(220, 53, 69)")
    expect(page.get_by_text("At least one uppercase letter")).to_have_css("color", "rgb(25, 135, 84)")
    expect(page.get_by_text("At least one lowercase letter")).to_have_css("color", "rgb(25, 135, 84)")
    expect(page.get_by_text("At least one number")).to_have_css("color", "rgb(25, 135, 84)")

# TC_Forget_11: Validate successful password reset with a valid New Password
def test_valid_new_password(forget_page_elements) -> None:
    page = forget_page_elements
    fill_email(page, EMAIL_VALID)
    fill_secret_code(page, SECRET_CODE_VALID)
    fill_passwords(page, CURRENT_PASSWORD, NEW_PASSWORD_VALID, NEW_PASSWORD_VALID)
    expect(page.get_by_text(SUCCESS_PASSWORD_CHANGED)).to_be_visible()
    expect(page.get_by_role("link", name="Return to Login")).to_be_visible()
import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def forget_page_elements(page: Page):
    page.goto("https://testerbud.com/forget-password")
    email_input = page.get_by_role("textbox", name="Enter your registered email")
    continue_button = page.get_by_role("button", name="Continue")
    back_to_login_button = page.get_by_role("button", name="Back to Login")
 
    return page, email_input, continue_button, back_to_login_button

# TC_Forget_01: Validate Error message if Email address left blank
def test_email_blank(forget_page_elements) -> None:
    page, email_input, continue_button, back_to_login_button = forget_page_elements
    continue_button.click()
    expect(page.get_by_text("Email is required")).to_be_visible()
    
# TC_Forget_02: Validate Error message if wrong Email address entered
def test_wrong_email(forget_page_elements) -> None:
    page, email_input, continue_button, back_to_login_button = forget_page_elements
    email_input.fill("user123@premiumbank.com")
    continue_button.click()
    expect(page.get_by_text("Email not found in our records")).to_be_visible()

# TC_Forget_03: Validate Error message if Secret Code left blank
def test_secret_code_blank(forget_page_elements) -> None:
    page, email_input, continue_button, back_to_login_button = forget_page_elements
    email_input.fill("user@premiumbank.com")
    continue_button.click()
    security_code_input =page.get_by_role("textbox", name="Enter security code")
    expect(security_code_input).to_have_value("")
    page.get_by_role("button", name="Verify Code").click()
    expect(page.get_by_text("Secret code is required")).to_be_visible()
    
# TC_Forget_04: Validate Error message if wrong Secret Code entered
def test_wrong_secret_code(forget_page_elements) -> None:
    page, email_input, continue_button, back_to_login_button = forget_page_elements
    email_input.fill("user@premiumbank.com")
    continue_button.click()
    security_code_input =page.get_by_role("textbox", name="Enter security code")
    security_code_input.fill("BANK12345") #Wrong secret code
    page.get_by_role("button", name="Verify Code").click()
    expect(page.get_by_text("Invalid secret code")).to_be_visible()

# TC_Forget_05: Validate Error message if Current Password left blank
def test_current_password_blank(forget_page_elements) -> None:
    page, email_input, continue_button, back_to_login_button = forget_page_elements
    email_input.fill("user@premiumbank.com")
    continue_button.click()
    security_code_input =page.get_by_role("textbox", name="Enter security code")
    security_code_input.fill("BANK1234") 
    page.get_by_role("button", name="Verify Code").click()
    current_password_input = page.get_by_role("textbox", name="Current password")
    expect(current_password_input).to_have_value("")
    page.get_by_role("button", name="Reset Password").click()
    expect(page.get_by_text("All fields are required")).to_be_visible()
    
# TC_Forget_06: Validate Error message if New Password left blank
def test_new_password_blank(forget_page_elements) -> None:
    page, email_input, continue_button, back_to_login_button = forget_page_elements
    email_input.fill("user@premiumbank.com")
    continue_button.click()
    security_code_input =page.get_by_role("textbox", name="Enter security code")
    security_code_input.fill("BANK1234") 
    page.get_by_role("button", name="Verify Code").click()
    current_password_input = page.get_by_role("textbox", name="Current password")
    current_password_input.fill("Bank@123")
    new_password_input = page.get_by_role("textbox", name="New password", exact=True)
    expect(new_password_input).to_have_value("")
    page.get_by_role("button", name="Reset Password").click()
    expect(page.get_by_text("All fields are required")).to_be_visible()
    
# TC_Forget_07: Validate Error message if Confirm New Password left blank
def test_confirm_new_password_blank(forget_page_elements) -> None:
    page, email_input, continue_button, back_to_login_button = forget_page_elements
    email_input.fill("user@premiumbank.com")
    continue_button.click()
    security_code_input =page.get_by_role("textbox", name="Enter security code")
    security_code_input.fill("BANK1234") 
    page.get_by_role("button", name="Verify Code").click()
    current_password_input = page.get_by_role("textbox", name="Current password")
    current_password_input.fill("Bank@123")
    new_password_input = page.get_by_role("textbox", name="New password", exact=True)
    new_password_input.fill("Brisbane@12345")
    confirm_new_password_input = page.get_by_role("textbox", name="Confirm new password")
    expect(confirm_new_password_input).to_have_value("")
    page.get_by_role("button", name="Reset Password").click()
    expect(page.get_by_text("All fields are required")).to_be_visible()
    
# TC_Forget_08: Validate error message if New and Confirm Password do not match
def test_confirm_new_old_password_not_match(forget_page_elements) -> None:
    page, email_input, continue_button, back_to_login_button = forget_page_elements
    email_input.fill("user@premiumbank.com")
    continue_button.click()
    security_code_input =page.get_by_role("textbox", name="Enter security code")
    security_code_input.fill("BANK1234") 
    page.get_by_role("button", name="Verify Code").click()
    current_password_input = page.get_by_role("textbox", name="Current password")
    current_password_input.fill("Bank@123")
    new_password_input = page.get_by_role("textbox", name="New password", exact=True)
    new_password_input.fill("Brisbane@12345")
    confirm_new_password_input = page.get_by_role("textbox", name="Confirm new password")
    confirm_new_password_input.fill("Brisbane@123456")
    page.get_by_role("button", name="Reset Password").click()
    expect(page.get_by_text("Passwords do not match")).to_be_visible()
    
# TC_Forget_09: Validate error message if New and Confirm Password do not meet password criteria
def test_confirm_new_old_password_not_meet_criteria(forget_page_elements) -> None:
    page, email_input, continue_button, back_to_login_button = forget_page_elements
    email_input.fill("user@premiumbank.com")
    continue_button.click()
    security_code_input =page.get_by_role("textbox", name="Enter security code")
    security_code_input.fill("BANK1234") 
    page.get_by_role("button", name="Verify Code").click()
    current_password_input = page.get_by_role("textbox", name="Current password")
    current_password_input.fill("Bank@123")
    new_password_input = page.get_by_role("textbox", name="New password", exact=True)
    new_password_input.fill("1234")
    confirm_new_password_input = page.get_by_role("textbox", name="Confirm new password")
    confirm_new_password_input.fill("1234")
    page.get_by_role("button", name="Reset Password").click()
    expect(page.get_by_text("Password does not meet requirements")).to_be_visible()
    
    
# TC_Forget_10: Validate password strength indicator when some criteria are met
def test_confirm_new_old_password_are_meet_some_criteria(forget_page_elements) -> None:
    page, email_input, continue_button, back_to_login_button = forget_page_elements
    email_input.fill("user@premiumbank.com")
    continue_button.click()
    security_code_input =page.get_by_role("textbox", name="Enter security code")
    security_code_input.fill("BANK1234") 
    page.get_by_role("button", name="Verify Code").click()
    current_password_input = page.get_by_role("textbox", name="Current password")
    current_password_input.fill("Bank@123")
    new_password_input = page.get_by_role("textbox", name="New password", exact=True)
    new_password_input.fill("Bb1234")
    confirm_new_password_input = page.get_by_role("textbox", name="Confirm new password")
    confirm_new_password_input.fill("Bb1234")

    expect(page.get_by_text("Minimum 8 characters")).to_have_css("color", "rgb(220, 53, 69)")
    expect(page.get_by_text("At least one special character")).to_have_css("color", "rgb(220, 53, 69)")

    expect(page.get_by_text("At least one uppercase letter")).to_have_css("color", "rgb(25, 135, 84)")
    expect(page.get_by_text("At least one lowercase letter")).to_have_css("color", "rgb(25, 135, 84)")
    expect(page.get_by_text("At least one number")).to_have_css("color", "rgb(25, 135, 84)")

# TC_Forget_11: Validate successful password reset with a valid New Password
def test_valid_new_password(forget_page_elements) -> None:
    page, email_input, continue_button, back_to_login_button = forget_page_elements
    email_input.fill("user@premiumbank.com")
    continue_button.click()
    security_code_input =page.get_by_role("textbox", name="Enter security code")
    security_code_input.fill("BANK1234") 
    page.get_by_role("button", name="Verify Code").click()
    current_password_input = page.get_by_role("textbox", name="Current password")
    current_password_input.fill("Bank@123")
    new_password_input = page.get_by_role("textbox", name="New password", exact=True)
    new_password_input.fill("Bank@12345")
    confirm_new_password_input = page.get_by_role("textbox", name="Confirm new password")
    confirm_new_password_input.fill("Bank@12345")
    page.get_by_role("button", name="Reset Password").click()
    expect(page.get_by_text("Password Changed Successfully!")).to_be_visible()
    back_to_login_link = page.get_by_role("link", name="Return to Login")
    expect(back_to_login_link).to_be_visible()
import pytest, re
from datetime import datetime
from playwright.sync_api import Page, expect

@pytest.fixture
def UI_page_elements(page: Page):
    page.goto("https://testerbud.com/practice-different-ui-elements")
    return page

## Basic elements  
def test_basic_UI_elements(UI_page_elements):
    page = UI_page_elements
    # Text Input
    text_input = page.get_by_role("textbox", name="Text Field (Input Box):")
    text_input.fill("hello123")
    expect(page.get_by_text("Output:hello123")).to_be_visible()
    
    
    # Text Area
    text_area = page.get_by_role("textbox", name="Text Area:")
    text_area.fill("This is a text field.")
    expect(page.get_by_text("Output:This is a text field.")).to_be_visible()
    
    
    # Button click
    button = page.get_by_role("button", name="Click Me")
    button.click()
    button.click()
    expect(page.get_by_text("Output:Clicked 2 times")).to_be_visible()
    
    
    # Checkbox
    checkbox = page.get_by_text("Single Option")
    expect(page.get_by_text("Output:Unchecked")).to_be_visible()
    checkbox.click()
    expect(page.get_by_text("Output:Checked")).to_be_visible()
    
    
    # Checkboxes (Multiple)
    multiple_checkboxes = page.locator("div").filter(has_text=re.compile(r"^Single Option$")).get_by_role("checkbox")
    expect(multiple_checkboxes).to_be_visible()
    op1 = page.locator("input[name=\"option1\"]")
    op2 = page.locator("input[name=\"option2\"]")
    op3 = page.locator("input[name=\"option3\"]")
    op2.check()
    op3.check()
    op1.check()
    op1.uncheck()
    expect(page.get_by_text("Checked: option2, option3")).to_be_visible()
    
    
    # Radio button
    page.locator("div").filter(has_text=re.compile(r"^Radio 3$")).get_by_role("radio").check()
    page.locator("div").filter(has_text=re.compile(r"^Radio 2$")).get_by_role("radio").check()
    expect(page.locator("div").filter(has_text=re.compile(r"^Output:Radio 2$")).locator("div")).to_be_visible()
    
    
    # Drop down
    page.get_by_label("Dropdown (Single Select):").select_option("UK")
    expect(page.locator("div").filter(has_text=re.compile(r"^UK$"))).to_be_visible()
    
    
    # Drop down Mutiple
    page.get_by_label("Dropdown (Multi-Select):").select_option(["Option C", "Option D"])
    page.get_by_label("Dropdown (Multi-Select):").select_option(["Option B", "Option C", "Option D"])
    expect(page.get_by_text("Option B, Option C, Option D")).to_be_visible()
 
 
## Interactive Elements   
def test_interactive_UI_elements(UI_page_elements): 
    page = UI_page_elements
    # Click me
    click_me = page.get_by_role("link", name="Click Me")
    expect(page.get_by_text("Click the link")).to_be_visible()
    click_me.click()
    expect(page.get_by_text("Link Clicked!")).to_be_visible()
    
    
    #image
    img = page.get_by_role("img", name="Placeholder")
    expect(page.get_by_text("Click the image")).to_be_visible()
    img.click()
    expect(page.get_by_text("Image Clicked!")).to_be_visible()
    
    
    # Table & Grid
    expect(page.get_by_text("Click a table header to \"sort\"")).to_be_visible()
    page.get_by_role("cell", name="Age").click()
    page.get_by_role("cell", name="ID").click()
    expect(page.get_by_text("Table sorted by ID")).to_be_visible()
    
    
    # Tooltip
    hover_me = page.get_by_text("Hover Me", exact=True)
    hover_me.hover()
    tooltip_id = hover_me.get_attribute("aria-describedby") 
    tooltip = page.locator(f"#{tooltip_id}")
    expect(page.get_by_text("This is a tooltip!")).to_be_visible()

    
    # Slider
    slider = page.get_by_role("slider")
    slider.fill("86")
    expect(page.get_by_text("Slider Value: 86")).to_be_visible()
    
    
    # Progress bars
    progress_bar = page.get_by_role("button", name="Increment Progress")
    progress_bar.click()
    progress_bar.click()
    expect(page.get_by_text("Progress: 50%")).to_be_visible()

    
## Complex UI Components
def test_complex_UI_elements(UI_page_elements):    
    page = UI_page_elements
    # show modal
    show_modal = page.get_by_role("button", name="Show Modal")
    show_modal.click()
    page.get_by_text("Close").click()
    output_show_modal = page.get_by_text("Click \"Show Modal\"")
    expect( output_show_modal).to_be_visible()
    
    show_modal.click()
    page.get_by_role("button", name="Save Changes").click()
    expect(output_show_modal).to_be_visible()
    
    show_modal.click()
    page.get_by_label("Close").click()
    expect(output_show_modal).to_be_visible()
    
    
    # date picker
    date = page.get_by_role("textbox", name="YYYY-MM-DD (Simulated)")
    date.fill("1998-02-02")
    expect(page.get_by_text("Output:1998-02-02")).to_be_visible()
    
    
    # File Upload & Download
    file_input = page.locator("input[type='file']")
    file_input.set_input_files(r"C:\Users\ASUS-USER\OneDrive\桌面\Cover letter.pdf")
    expect(page.get_by_text('Output:File "Cover letter.pdf" selected')).to_be_visible()

        
    # Drag and drop
    drag_me = page.locator(".border.p-2.text-center.draggable")
    drop_here = page.locator(".border.p-2.mt-2.text-center.droppable")
    
    drag_me.wait_for(state="visible")
    drop_here.wait_for(state="visible")
    drag_me.scroll_into_view_if_needed()
    drop_here.scroll_into_view_if_needed()
    
    drag_me.drag_to(drop_here)

    output = page.locator("text=Output:Dropped!")
    output.wait_for(state="visible", timeout=10000)
    expect(output).to_be_visible()

    page.get_by_role("button", name="Simulate Download").click()
    def handle_dialog(dialog):
        print("Alert message:", dialog.message)
        dialog.accept()  # or dialog.dismiss()

    page.on("dialog", handle_dialog)

    # Iframe
    #expect(page.locator("iframe[title=\"iframe-practice\"]").content_frame.get_by_text("Example Domain This domain is")).to_be_visible()
    #expect(page.get_by_text("Output:Iframe loaded")).to_be_visible()
    
## Advanced UI Elements
def test_advanced_UI_elements(UI_page_elements):    
    page = UI_page_elements
    page.get_by_role("button", name="Update Content").click()

    # Dynamic Content (Simulated):
    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p").lstrip("0")
    expect(page.get_by_text("Updated at {}".format(current_time))).to_be_visible()
    
    
    # Notifications & Toast Messages
    show_notification = page.get_by_role("button", name="Show Notification")
    show_notification.click()
    expect(page.get_by_text("Notification shown")).to_be_visible()
    
    
    # Tabs
    page.get_by_role("button", name="Tab 1").click()
    page.get_by_role("button", name="Tab 2").click()
    expect(page.get_by_text("Active Tab: tab2")).to_be_visible()
    
    
    # Accordion
    page.get_by_role("button", name="Accordion Item #2").click()
    expect(page.get_by_text("Content of Accordion Item #2")).to_be_visible()
    expect(page.get_by_text("Accordion item \"item2\" is open")).to_be_visible()
    
    
    # Virtual Scrolling (Simulated)
    container = page.locator(".border.rounded.p-2.overflow-auto")
    container.hover()
    page.mouse.wheel(0, 200)  # scroll down
    expect(page.get_by_text("Scroll Position: 200")).to_be_visible()

     
    

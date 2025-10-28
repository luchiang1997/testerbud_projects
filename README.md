# Project Automation - TesterBud (In progress)

Automated UI testing project for [TesterBud Practice](https://testerbud.com/practice-forms), built with **Python + Playwright + pytest**.

This suite covers multiple interactive UI scenarios and supports **parallel execution** with **HTML reporting**.

## Requirements

- Python 3.10+ (or compatible)
- Playwright
- pytest
- pytest-playwright
- (optional) **pytest-xdist** → for parallel test execution  
- (optional) **pytest-html** → for HTML report generation

## Setup

**1. Clone the repository** (if not already):

```bash
git clone https://github.com/luchiang1997/testerbud_projects.git
cd testerbud_projects
```

**2. Create a virtual environment:**
```bash
python -m venv venv
```

**3. Activate the virtual environment:**
```bash
# Windows
.\venv\Scripts\activate.bat

# Linux / macOS
source venv/bin/activate
```

**4. Install dependencies:**
```bash
pip install -r requirements.txt
```

**5. Install Playwright browsers:**
```bash
playwright install
```

## Running Tests
Tests are located in the tests/ folder. Run all tests with:
```bash
pytest
```

Run specific test function
```bash
pytest tests/ui/test_UI_elements.py::test_complex_UI_elements
```

This project supports parallel test execution via **pytest-xdist**:
```bash
pytest -n auto
```

Example with **HTML report**:
```bash
pytest -n auto --html=reports/report.html --self-contained-html
```

## Folder Structure
```bash
testerbud_projects/
├── tests/
│   ├── auth/
│   │   │── test_forget_password.py
│   │   │── test_login.py
│   │   └── test_register.py
│   ├── e-commerce/
│   │   │── test_card.py
│   │   │── test_e2e_shopping.py
│   │   │── test_inventory.py
│   │   └── test_shipping.py
│   ├── flight_booking/
│   │   │── test_e2e_booking.py
│   │   │── test_flight_searching_form.py
│   │   └── test_payment.py
│   ├── form/
│   │   └── test_webform.py
│   └── ui/
│       └── test_UI_elements.py
├── conftest.py
├── report.html
├── requirements.txt
├── pytest.ini
└── README.md
```

## Output
<img width="624" height="888" alt="image" src="https://github.com/user-attachments/assets/9e08aba6-6f5a-4ecd-9c99-f21feb64b2cc" />
<img width="620" height="891" alt="image" src="https://github.com/user-attachments/assets/85099297-29e8-4572-a41b-01a92a9d1236" />

## 💡 Learnings & Reflections

- Explored various **UI elements** and tested multiple **real-world scenarios** to simulate practical automation challenges.  
- Experimented with both **tuple/unpacking** and **dictionary-based** approaches for handling test data.  
  After hands-on experience, found that the **dictionary-based method** provides better **maintainability and scalability**.  
- Implemented **parallel execution** using multi-core processing to significantly **reduce total runtime**.  
- Utilised **GitHub Copilot AI** to assist in **code refactoring** and receive intelligent **suggestions** for improving structure and readability.





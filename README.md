# Project Automation - TesterBud (In progress)

This project contains Playwright automation tests for several practice scenarios on [TesterBud](https://testerbud.com/practice-forms).

## Requirements

- Python 3.10+ (or compatible)
- Playwright
- pytest
- pytest-playwright

## Setup

**1. Clone the repository** (if not already):

```bash
git clone https://github.com/luchiang1997/testerbud_projects.git
cd testerbud_projects/project_form
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

By default, pytest.ini will:

  - Run all files matching `test_*.py` in `tests/`

  - Open Chromium in headed mode

  - Apply a slow motion of 200ms (`--slowmo=200`)

  - Generate an HTML report at `reports/report.html`

To run a specific test file:
```bash
pytest tests/test_webform.py
```



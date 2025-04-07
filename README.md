# Diplom_SkyPro

# Kinopoisk API and UI Tests

This project contains automated tests for Kinopoisk API and UI using Python, Selenium, Requests, Pytest and Allure.

## Project Structure
project/
├── config/ # Configuration files
│ ├── environment.py # Environment settings (URLs, etc.)
│ └── test_data.py # Test data (logins, passwords, etc.)
│
├── tests/ # Test files
│ ├── test_api.py # API tests
│ └── test_ui.py # UI tests
│
├── conftest.py # Pytest configuration
├── pytest.ini # Pytest settings
├── README.md # Project documentation
└── requirements.txt # Python dependencies

## How to Run Tests

1. Install dependencies:
```bash
pip install -r requirements.txt


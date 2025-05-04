import pytest
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption("--ui", action="store_true", help="run UI tests")
    parser.addoption("--api", action="store_true", help="run API tests")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--ui"):
        skip_api = pytest.mark.skip(reason="Skipping API tests")
        for item in items:
            if "test_api" in item.nodeid:
                item.add_marker(skip_api)
    elif config.getoption("--api"):
        skip_ui = pytest.mark.skip(reason="Skipping UI tests")
        for item in items:
            if "test_ui" in item.nodeid:
                item.add_marker(skip_ui)

def pytest_configure(config):
    config.option.allure_report_dir = './allure-results'


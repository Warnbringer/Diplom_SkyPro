# Diplom_SkyPro

# Kinopoisk API and UI Tests

Этот проект содержит автоматизированные тесты для API
и пользовательского интерфейса Кинопоиска с использованием
Python, Selenium, Requests, Pytest и Allure.

## Структура проекта
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

## Инструкция по запуску тестов

1. Установка зависимостей
Сначала установите все необходимые пакеты:
pip install selenium pytest allure-pytest requests webdriver-manager
2. Запуск тестов
Базовый запуск всех тестов:
pytest tests/ --alluredir=./allure-results -v
Запуск только UI-тестов:
pytest tests/test_ui.py::TestKinopoiskSearch::test_search_by_full_title -v
Запуск только API-тестов:
pytest tests/test_ui.py -k "not test_search_by_full_title" -v
3. Генерация отчета Allure
После выполнения тестов создайте отчет:
allure serve ./allure-results

## Важные замечания

Убедитесь, что у вас установлен Chrome браузер

Для автоматической загрузки WebDriver можно использовать webdriver-manager, 
который уже включен в зависимости

При проблемах с запуском Chrome попробуйте добавить опции:

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")





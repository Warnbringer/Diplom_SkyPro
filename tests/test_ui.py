import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import allure

# Конфигурация
KP_API_BASE_URL = "https://api.kinopoisk.dev/v1.4"
KP_API_TOKEN = "B1J38JK-1VE4P0A-JB38DGJ-YMPJPKE"
KP_UI_URL = "https://www.kinopoisk.ru/"
WAIT_TIMEOUT = 15

@pytest.fixture(scope="module")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def api_headers():
    return {"X-API-KEY": KP_API_TOKEN}

def make_api_request(endpoint, params=None, headers=None):
    url = f"{KP_API_BASE_URL}/{endpoint}"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def wait_and_click(driver, locator, timeout=WAIT_TIMEOUT):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )
    element.click()
    return element


def wait_and_send_keys(driver, locator, keys, timeout=WAIT_TIMEOUT):
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )
    element.clear()
    element.send_keys(keys)
    return element


def accept_cookies_if_present(browser):
    try:
        cookie_btn = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Принять')]"))
        )
        cookie_btn.click()
    except:
        pass


@allure.feature("Поиск на Кинопоиске")
class TestKinopoiskSearch:

    @allure.story("Поиск по полному названию фильма")
    def test_search_by_full_title(self, browser, api_headers):
        movie_name = "Интерстеллар"

        with allure.step("UI: Выполняем поиск"):
            browser.get(KP_UI_URL)
            accept_cookies_if_present(browser)

            # Поиск поля ввода с несколькими вариантами локаторов
            search_locators = [
                (By.NAME, "kp_query"),
                (By.CSS_SELECTOR, "input[placeholder='Фильмы, сериалы, персоны']"),
                (By.XPATH, "//input[@type='text' and contains(@class, 'search')]")
            ]

            for locator in search_locators:
                try:
                    search_field = wait_and_send_keys(browser, locator, movie_name, 5)
                    break
                except:
                    continue
            else:
                pytest.fail("Не удалось найти поле поиска")

            # Отправка формы поиска
            try:
                search_field.send_keys(Keys.RETURN)
            except:
                try:
                    search_button = WebDriverWait(browser, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[.//*[contains(@class, 'search')]]"))
                    )
                    search_button.click()
                except:
                    pytest.fail("Не удалось отправить форму поиска")

            # Ожидание результатов
            WebDriverWait(browser, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".search_results, .empty-results"))
            )

        with allure.step("API: Проверяем результаты"):
            api_params = {"query": movie_name, "limit": 5}
            api_response = make_api_request("movie/search", api_params, api_headers)
            assert api_response["total"] > 0, "API не вернул результаты"

    @allure.story("Фильтрация по жанру и году")
    def test_filter_by_genre_and_year(self, api_headers):
        with allure.step("API: Получаем фильмы по жанру и году"):
            api_params = {
                "genres.name": "+фантастика",
                "year": "2014",
                "limit": 3
            }
            api_response = make_api_request("movie", api_params, api_headers)
            assert len(api_response["docs"]) > 0

    @allure.story("Поиск с исключением жанра")
    def test_search_with_excluded_genre(self, api_headers):
        with allure.step("API: Ищем драмы без криминала"):
            api_params = {
                "genres.name": "+драма",
                "genres.name": "!криминал",
                "limit": 3
            }
            api_response = make_api_request("movie", api_params, api_headers)
            assert len(api_response["docs"]) > 0

    @allure.story("Фильтрация по рейтингу")
    def test_filter_by_rating(self, api_headers):
        with allure.step("API: Ищем фильмы с рейтингом 7-10"):
            api_params = {"rating.kp": "7-10", "limit": 3}
            api_response = make_api_request("movie", api_params, api_headers)
            assert len(api_response["docs"]) > 0

    @allure.story("Комплексный поиск с несколькими параметрами")
    def test_complex_search(self, api_headers):
        with allure.step("API: Комплексный поиск"):
            api_params = {
                "year": "2020-2023",
                "rating.kp": "7-10",
                "genres.name": "+фантастика",
                "genres.name": "!ужасы",
                "limit": 3
            }
            api_response = make_api_request("movie", api_params, api_headers)
            assert len(api_response["docs"]) > 0

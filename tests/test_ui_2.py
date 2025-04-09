import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


@pytest.fixture(scope="module")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@allure.feature("Тесты Кинопоиска")
class TestKinopoiskUI:

    @allure.story("Поиск фильма по названию")
    def test_search_movie(self, browser):
        with allure.step("1. Открыть главную страницу"):
            browser.get("https://www.kinopoisk.ru/")

        with allure.step("2. Ввести название фильма"):
            search_field = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.NAME, "kp_query"))
            )
            search_field.send_keys("Интерстеллар")

        with allure.step("3. Нажать кнопку поиска"):
            search_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            search_button.click()

        with allure.step("4. Проверить результаты"):
            results = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search_results .name"))
            )
            assert any("Интерстеллар" in result.text for result in results)

    @allure.story("Проверка перехода на страницу фильма")
    def test_open_movie_page(self, browser):
        with allure.step("1. Открыть страницу топ-250"):
            browser.get("https://www.kinopoisk.ru/top/")

        with allure.step("2. Выбрать первый фильм из списка"):
            first_movie = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-tid='d4e8d214']"))
            )
            movie_name = first_movie.text
            first_movie.click()

        with allure.step("3. Проверить заголовок на странице фильма"):
            title = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            assert movie_name in title.text

    @allure.story("Проверка фильтрации по жанру")
    def test_filter_by_genre(self, browser):
        with allure.step("1. Открыть страницу с фильмами"):
            browser.get("https://www.kinopoisk.ru/lists/movies/")

        with allure.step("2. Выбрать жанр 'комедия'"):
            genre_button = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.styles_selectButton__4xHt7.styles_button__3dBmr.styles_thin__zGEcp"))
            )
            genre_button.click()

            comedy_checkbox = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "label[data-tid='68e7193']"))
            )
            comedy_checkbox.click()

        with allure.step("4. Проверить результаты"):
            WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".styles_root__ti07r"))
            )
            # Дополнительная проверка жанра в карточках фильмов

    @allure.story("Тест авторизации на Кинопоиске")
    def test_auth_login(self, browser):
        with allure.step("1. Открыть страницу авторизации"):
            browser.get("https://passport.yandex.ru/auth?retpath=https%3A%2F%2Fwww.kinopoisk.ru%2F")

        with allure.step("2. Найти поле ввода логина"):
            email_field = WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input#passp-field-login"))
            )

        with allure.step("3. Ввести email"):
            email_field.clear()
            email_field.send_keys("warnbringer93")

        with allure.step("4. Нажать кнопку 'Войти'"):
            submit_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            submit_button.click()

        with allure.step("5. Проверить переход на страницу пароля"):
            WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.NAME, "passwd"))
            )

        with allure.step("5. Ввести пароль"):
            password_field = WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.NAME, "passwd"))
            )
            password_field.clear()
            password_field.send_keys("!Lost4815162342")

            submit_button = WebDriverWait(browser, 160).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            submit_button.click()

    @allure.story("Проверка поиска с пустым запросом")
    def test_empty_search(self, browser):
        with allure.step("1. Открыть главную страницу"):
            browser.get("https://www.kinopoisk.ru/")

        with allure.step("2. Отправить пустой поисковый запрос"):
            search_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.NAME, "kp_query"))
            )
            search_button.click()

        with allure.step("3. Проверить переход на страницу поиска по параметрам"):
            search_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[contains(@class, 'search-form-submit-button__icon')]/ancestor::button")
                )
            )
            search_button.click()

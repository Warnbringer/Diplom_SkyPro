import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def api_url():
    return "https://api.kinopoisk.dev/v1.4/movie"


@allure.feature("Поиск фильмов")
class TestMovieSearch:

    @allure.story("Ввод названия фильма")
    @allure.description("Проверка, что при вводе названия фильма отображаются соответствующие результаты")
    def test_search_by_full_title(self, browser):
        with allure.step("Открыть страницу поиска"):
            browser.get("https://www.kinopoisk.ru/")

        with allure.step("Ввести полное название фильма"):
            search_field = browser.find_element(By.NAME, "kp_query")
            search_field.send_keys("Интерстеллар")

        with allure.step("Нажать кнопку поиска"):
            search_button = browser.find_element(By.CSS_SELECTOR,
                                                 'button .search-form-submit-button__icon').find_element(By.XPATH,
                                                                                                         './..')
            search_button.click()
#
#         with allure.step("Проверить результаты поиска"):
#             results = WebDriverWait(browser, 10).until(
#                 EC.presence_of_all_elements_located((By.CLASS_NAME, "movie-result"))
#             assert len(results) > 0
#             assert "Интерстеллар" in results[0].text \
#  \
#                    @ allure.story("Ввод части названия фильма") \
#                    @ allure.description(
#                 "Проверка, что при вводе части названия фильма отображаются соответствующие результаты")
#
#     def test_search_by_partial_title(self, browser):
#         with allure.step("Открыть страницу поиска"):
#             browser.get("https://api.kinopoisk.dev/v1.4/movie")
#
#         with allure.step("Ввести часть названия фильма"):
#             search_input = browser.find_element(By.ID, "search-input")
#             search_input.send_keys("Интер")
#
#         with allure.step("Нажать кнопку поиска"):
#             browser.find_element(By.ID, "search-button").click()
#
#         with allure.step("Проверить результаты поиска"):
#             results = WebDriverWait(browser, 10).until(
#                 EC.presence_of_all_elements_located((By.CLASS_NAME, "movie-result")))
#             assert len(results) > 0
#             assert any("Интер" in result.text for result in results)
#
#     @allure.story("НФКП 19. Использование фильтров")
#     @allure.description("Проверка работы фильтров по жанру, году и рейтингу")
#     def test_search_with_filters(self, browser, api_url):
#         with allure.step("Открыть страницу поиска"):
#             browser.get("https://api.kinopoisk.dev/v1.4/movie")
#
#         with allure.step("Применить фильтры"):
#             # Выбрать жанр "Фантастика"
#             browser.find_element(By.XPATH, "//select[@id='genre']/option[text()='Фантастика']").click()
#             # Выбрать год выпуска "2014"
#             browser.find_element(By.XPATH, "//select[@id='year']/option[text()='2014']").click()
#             # Установить минимальный рейтинг 8
#             browser.find_element(By.ID, "min-rating").send_keys("8")
#
#         with allure.step("Нажать кнопку поиска"):
#             browser.find_element(By.ID, "search-button").click()
#
#         with allure.step("Проверить результаты через UI"):
#             results = WebDriverWait(browser, 10).until(
#                 EC.presence_of_all_elements_located((By.CLASS_NAME, "movie-result")))
#             assert len(results) > 0
#
#         with allure.step("Проверить результаты через API"):
#             params = {
#                 "genre": "sci-fi",
#                 "year": 2014,
#                 "min_rating": 8
#             }
#             response = requests.get(api_url, params=params)
#             api_results = response.json()
#             assert len(api_results) == len(results)
#
#     @allure.story("Поиск несуществующего фильма")
#     @allure.description("Проверка отображения сообщения, когда фильм не найден")
#     def test_search_non_existing_movie(self, browser):
#         with allure.step("Открыть страницу поиска"):
#             browser.get("https://api.kinopoisk.dev/v1.4/movie")
#
#         with allure.step("Ввести несуществующее название"):
#             search_input = browser.find_element(By.ID, "search-input")
#             search_input.send_keys("Несуществующий фильм 12345")
#
#         with allure.step("Нажать кнопку поиска"):
#             browser.find_element(By.ID, "search-button").click()
#
#         with allure.step("Проверить сообщение об ошибке"):
#             error_message = WebDriverWait(browser, 10).until(
#                 EC.visibility_of_element_located((By.ID, "error-message")))
#             assert error_message.text == "Фильм не найден"
#
#     @allure.story("Поиск с пустым полем")
#     @allure.description("Проверка отображения сообщения при пустом поисковом запросе")
#     def test_search_with_empty_query(self, browser):
#         with allure.step("Открыть страницу поиска"):
#             browser.get("https://api.kinopoisk.dev/v1.4/movie")
#
#         with allure.step("Оставить поле поиска пустым"):
#             search_input = browser.find_element(By.ID, "search-input")
#             search_input.clear()
#
#         with allure.step("Нажать кнопку поиска"):
#             browser.find_element(By.ID, "search-button").click()
#
#         with allure.step("Проверить сообщение об ошибке"):
#             error_message = WebDriverWait(browser, 10).until(
#                 EC.visibility_of_element_located((By.ID, "empty-query-message")))
#             assert "необходимо ввести данные для поиска" in error_message.text
#
#
# @allure.feature("Переход на страницу фильма")
# class TestMoviePage:
#
#     @allure.story("Переход на страницу фильма")
#     @allure.description("Проверка перехода на страницу фильма из результатов поиска")
#     def test_open_movie_page_from_search(self, browser):
#         with allure.step("Выполнить поиск фильма"):
#             browser.get("https://api.kinopoisk.dev/v1.4/movie")
#             search_input = browser.find_element(By.ID, "search-input")
#             search_input.send_keys("Интерстеллар")
#             browser.find_element(By.ID, "search-button").click()
#
#         with allure.step("Выбрать первый результат из списка"):
#             first_result = WebDriverWait(browser, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, "movie-result")))
#             first_result.click()
#
#         with allure.step("Проверить, что открылась страница фильма"):
#             WebDriverWait(browser, 10).until(
#                 EC.url_contains("/movie/"))
#             assert "Интерстеллар" in browser.find_element(By.TAG_NAME, "h1").text
#             assert browser.find_element(By.CLASS_NAME, "movie-info")
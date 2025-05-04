import pytest
import requests
import allure
from config.environment import Environment
from config.test_data import TestData


@allure.feature("API Tests")
class TestKinopoiskAPI:
    @allure.story("Поиск фильма по названию")
    def test_search_movie_by_title(self):
        with allure.step("Отправка GET-запроса на поиск фильма по названию"):
            url = f"{Environment.BASE_API_URL}/search"
            params = {
                "query": TestData.MOVIE_TITLE,
                "token": Environment.API_KEY
            }
            response = requests.get(url, params=params)

        with allure.step("Проверка статус-кода ответа и его содержания"):
            assert response.status_code == 200
            assert TestData.MOVIE_TITLE.lower() in response.text.lower()

    @allure.story("Поиск фильма по ID-идентификатору")
    def test_get_movie_by_id(self):
        with allure.step("Отправить GET запрос на поиск фильма по ID"):
            url = f"{Environment.BASE_API_URL}/{TestData.MOVIE_ID}"
            params = {"token": Environment.API_KEY}
            response = requests.get(url, params=params)

        with allure.step("Проверка статус-кода ответа и его содержания"):
            assert response.status_code == 200
            assert response.json()["id"] == int(TestData.MOVIE_ID)

    @allure.story("Поиск фильма по нескольким параметрам")
    def test_search_movie_with_multiple_params(self):
        with allure.step("Отправка GET-запроса с несколькими параметрами"):
            url = f"{Environment.BASE_API_URL}/search"
            params = {
                "query": TestData.MOVIE_TITLE,
                "year": TestData.MOVIE_YEAR,
                "token": Environment.API_KEY
            }
            response = requests.get(url, params=params)

        with allure.step("Проверка статус-кода ответа и его содержания"):
            assert response.status_code == 200
            data = response.json()
            assert any(movie["name"] == TestData.MOVIE_TITLE and
                       str(movie["year"]) == TestData.MOVIE_YEAR
                       for movie in data.get("docs", []))

    @allure.story("Поиск фильма с неправильным методом")
    def test_search_movie_with_wrong_method(self):
        with allure.step("Отправка запроса POST на конечную точку поиска"):
            url = f"{Environment.BASE_API_URL}/search"
            params = {
                "query": TestData.MOVIE_TITLE,
                "token": Environment.API_KEY
            }
            response = requests.post(url, params=params)

        with allure.step("Проверка ответа об ошибке"):
            assert response.status_code == 404

    @allure.story("Получить фильм с несуществующим идентификатором")
    def test_get_non_existent_movie(self):
        with allure.step("Отправка GET-запроса с несуществующим ID"):
            url = f"{Environment.BASE_API_URL}/{TestData.INVALID_MOVIE_ID}"
            params = {"token": Environment.API_KEY}
            response = requests.get(url, params=params)

        with allure.step("Проверка ответа об ошибке"):
            assert response.status_code == 404
            assert "not found" in response.text.lower()
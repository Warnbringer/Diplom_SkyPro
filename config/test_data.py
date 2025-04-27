class TestData:
    # API test data
    MOVIE_TITLE = "Титаник"
    MOVIE_ID = "2213"
    MOVIE_YEAR = "1997"
    INVALID_MOVIE_ID = "999934"
    PARTIAL_MOVIE_TITLE = "Тит"
    NON_EXISTENT_MOVIE = "Несуществующий фильм"
    MOVIE_FOR_TICKET = "duna"  # slug для URL

    # Ticket test data
    TICKET_DATE = "2025-02-15"
    SEAT_NUMBER = "A5"

    # Auth test data
    VALID_LOGIN = "######"
    VALID_PASSWORD = "######"
    INVALID_LOGIN = "wrong@example.com"
    INVALID_PASSWORD = "wrongpass"

    BASE_API_URL = "https://api.kinopoisk.dev/v1.4"
    url = f"{BASE_API_URL}/movie/search"  # Полный URL: https://api.kinopoisk.dev/v1.4/movie/search

    BASE_UI_URL = "https://passport.yandex.ru"
    url = f"{BASE_UI_URL}/login"  # Полный URL: https://api.kinopoisk.dev/v1.4/movie/search
    KP_API_TOKEN = "B1J38JK-1VE4P0A-JB38DGJ-YMPJPKE"

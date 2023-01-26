from os import getcwd


class Kernel:

    """
    Основные настройки ядра
    """

    DEBUG = True  # Debug режим в Flask

    IP = '127.0.0.1'  # IP адрес сервера
    PORT = '5000'  # Port сервера (80 - стандартный)


class Database:

    """
        Настройки для подключения в базе данных
    """

    URI = 'mongodb://localhost:27017/'  # Ссылается на базу данных
    NAME = "oasis_core"  # Имя базы данных


class Path:

    """
        Настройки для путей к эндпоинтам и т.д.
    """

    TO_DATABASE = "/database/db"  # Где будут находиться эндпоинты
    TO_ROOT = getcwd()  # Путь к ядру

    TO_BACKUP = "http://127.0.0.1:5000"  # Расположение бэкапов
    TO_SONG = "http://127.0.0.1:5000/song"  # Расположение музыки


class Security:
    """
        Настройки для более максимальной защиты ядра
    """

    SITE_KEY = ""  # Используется hcaptcha (https://www.hcaptcha.com/)
    SECRET_KEY = ""

    MAIL_SERVER = "mail.jino.ru"
    MAIL_LOGIN = "admin@complextech-music.tk"
    MAIL_PASSWORD = "password"

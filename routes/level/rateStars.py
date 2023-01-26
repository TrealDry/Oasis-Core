from . import level
from utils import *
from config import *
from flask import request


@level.route(f"{Path.TO_DATABASE}/rateGJStars211.php", methods=("POST", "GET"))
def rate_stars():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    return "1"  # Заглушка

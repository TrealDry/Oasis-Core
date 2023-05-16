from utils import *
from . import account
from config import Path


@account.route(f"{Path.TO_DATABASE}/accounts/loginGJAccount.php", methods=("POST", "GET"))
def login_account():
    if not secret_check(get_arg("secret"), 1):
        return "-1"

    username = get_arg("userName")
    password = get_arg("password")

    account_id = account_db.find_one({"username": {"$regex": f"^{username}$", '$options': 'i'}})["account_id"]
    user_id = account_db.find_one({"account_id": account_id})["user_id"]

    # Проверка на длину строки
    if len(username) > 15 or len(password) > 20:
        return "-1"

    if check_password(account_id, password, False, ip=get_ip()):
        return f"{account_id},{user_id}"

    return "-1"

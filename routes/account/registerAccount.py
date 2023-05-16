from utils import *
from time import time
from . import account
from random import randint
from threading import Thread
from config import Path, Security, Kernel


@account.route(f"{Path.TO_DATABASE}/accounts/registerGJAccount.php", methods=("POST", "GET"))
def register_account():
    if not secret_check(get_arg("secret"), 1):
        return "-1"

    username = get_arg("userName")
    password = get_arg("password")
    email = get_arg("email")

    # Проверка на длину строки
    if len(username) > 15 or len(password) > 20 or \
       len(email) > 32:
        return "-1"

    # Проверка, есть ли такой ник и почта
    if account_db.count_documents({"username": {"$regex": f"^{username}$", '$options': 'i'}}) == 1 or \
       account_db.count_documents({"email": {"$regex": f"^{email}$", '$options': 'i'}}) == 1:
        return "-1"

    confirmation_code = randint(100000000000, 999999999999)

    mail_t = Thread(target=sending_letter, args=(1, {
        "sender": Security.MAIL_LOGIN,
        "recipient": email,
        "message": f"https://{Kernel.IP}/activate_account?code={str(confirmation_code)}"
    },))

    mail_t.start()

    sample_account = {
        "account_id": last_id(account_db, "account_id"),
        "user_id": 0,
        "username": username,
        "password": hash_password(password),
        "email": email,
        "discord_id": 0,
        "confirmation_code": confirmation_code,
        "confirmation_code_discord": 0,
        "date": int(time()),
        "valid": 0
    }

    account_db.insert_one(sample_account)
    return "1"

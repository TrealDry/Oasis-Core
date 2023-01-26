from . import misc
from utils import *
from config import *
from flask import request


@misc.route("/database/accounts/syncGJAccountNew.php", methods=("POST", "GET"))
def sync_account():
    if not secret_check(request.values.get("secret"), 1):
        return "-1"

    username = get_arg("userName")
    password = get_arg("password")

    try:
        account_id = user_db.find_one({"username": {"$regex": f"(?i){username}"}})["account_id"]
    except TypeError:
        return "-1"

    if not check_password(account_id, password, False, ip=get_ip()):
        return "-1"

    try:
        with open(f"{Path.TO_ROOT}/data/account/{str(account_id)}.account", "r") as f:
            save_data = f.read()
    except FileNotFoundError:
        return "-1"

    return save_data + ";21;30;a;a"

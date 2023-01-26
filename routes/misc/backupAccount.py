from . import misc
from utils import *
from config import *
from flask import request


maximum_backup_size = 15728640


@misc.route("/database/accounts/backupGJAccountNew.php", methods=("POST", "GET"))
def backup_account():
    if not secret_check(request.values.get("secret"), 1):
        return "-1"

    username = get_arg("userName")
    password = get_arg("password")

    try:
        account_id = user_db.find_one({"username": {"$regex": f"(?i){username}"}})["account_id"]
    except TypeError:
        return "-1"

    save_data = get_arg("saveData")

    if not check_password(account_id, password, False, ip=get_ip()):
        return "-1"

    with open(f"{Path.TO_ROOT}/data/account/{str(account_id)}.account", "w") as f:
        f.write(save_data)

    return "1"

from . import level
from utils import *
from config import *
from flask import request


@level.route(f"{Path.TO_DATABASE}/rateGJDemon21.php", methods=("POST", "GET"))
def rate_demon():
    if not secret_check(request.values.get("secret"), 4):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    level_id = int_arg(get_arg("levelID"))
    rating = int_arg(get_arg("rating"))

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    if roleassing_db.count_documents({
        "account_id": account_id
    }) == 0:
        return "1"

    role = tuple(role_db.find({"role_id": roleassing_db.find_one({"account_id": account_id})["role_id"]}))

    if role[0]["command_type_demon"] == 0:
        return str(level_id)

    level_db.update_one({"level_id": level_id}, {"$set": {
        "demon_type": rating
    }})

    return str(level_id)

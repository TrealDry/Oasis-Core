from . import misc
from utils import *
from config import *
from flask import request


@misc.route(f"{Path.TO_DATABASE}/requestUserAccess.php", methods=("POST", "GET"))
def request_user_access():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    if roleassing_db.count_documents({
        "account_id": account_id
    }) == 0:
        return "-1"

    role = tuple(role_db.find({"role_id": roleassing_db.find_one({"account_id": account_id})["role_id"]}))

    user_db.update_one({"account_id": account_id}, {"$set": {
        "mod_level": role[0]["role_badge_mod"],
        "color_comment": role[0]["role_color"]
    }})

    return str(role[0]["role_badge_mod"])

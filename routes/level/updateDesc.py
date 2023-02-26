from . import level
from utils import *
from config import *


@level.route(f"{Path.TO_DATABASE}/updateGJDesc20.php", methods=("POST", "GET"))
def update_desc():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    level_id = int_arg(get_arg("levelID"))
    level_desc = get_arg("levelDesc")

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    if not limit_check(len(base64_decode(level_desc)), 140):
        return "-1"

    if level_db.count_documents({
        "account_id": account_id,
        "level_id": level_id,
        "deleted": 0
    }) == 0:
        return "-1"

    level_db.update_one({"level_id": level_id}, {"$set": {
        "level_desc": level_desc
    }})

    return "1"

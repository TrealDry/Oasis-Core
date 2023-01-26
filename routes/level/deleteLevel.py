from . import level
from utils import *
from config import *
from flask import request


@level.route(f"{Path.TO_DATABASE}/deleteGJLevelUser20.php", methods=("POST", "GET"))
def delete_level():
    if not secret_check(request.values.get("secret"), 3):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    level_id = int_arg(get_arg("levelID"))

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    if level_db.count_documents({
        "level_id": level_id,
        "delete_prohibition": 0,
        "star": {"$lt": 1},
        "deleted": 0
    }):

        with open(f"{Path.TO_ROOT}/data/level/{str(level_id)}.level", "w") as level_file:
            level_file.write("")

        level_db.update_one({"level_id": level_id}, {"$set": {
            "deleted": 1
        }})

        levelcomment_db.update_many({"level_id": level_id}, {"$set": {
            "is_deleted": 1
        }})

    return "1"

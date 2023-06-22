from utils import *
from config import *
from . import comment
from flask import request


@comment.route(f"{Path.TO_DATABASE}/deleteGJComment20.php", methods=("POST", "GET"))
def delete_comment():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    level_id = int_arg(get_arg("levelID"))
    comment_id = int_arg(get_arg("commentID"))

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    if levelcomment_db.count_documents({
        "comment_id": comment_id, "level_id": level_id, "is_deleted": 0
    }) == 1:
        if level_db.count_documents({
            "account_id": account_id,
            "level_id": level_id
        }) == 1:
            pass
        elif levelcomment_db.count_documents({
            "account_id": account_id,
            "comment_id": comment_id,
            "level_id": level_id
        }) == 0:
            return "-1"
    else:
        return "-1"

    levelcomment_db.update_one({"comment_id": comment_id}, {"$set": {
        "is_deleted": 1
    }})

    return "1"

from utils import *
from config import *
from . import comment
from flask import request


@comment.route(f"{Path.TO_DATABASE}/deleteGJAccComment20.php", methods=("POST", "GET"))
def delete_account_comment():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    comment_id = int_arg(get_arg("commentID"))

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    if usercomment_db.count_documents({
        "account_id": account_id,
        "comment_id": comment_id,
        "is_deleted": 0
    }) == 0:
        return "-1"

    usercomment_db.update_one({"comment_id": comment_id}, {"$set": {
        "is_deleted": 1
    }})

    return "1"

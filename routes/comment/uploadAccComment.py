from utils import *
from config import *
from . import comment
from time import time
from flask import request


@comment.route(f"{Path.TO_DATABASE}/uploadGJAccComment20.php", methods=("POST", "GET"))
def upload_account_comment():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    acc_comment = get_arg("comment")

    if not check_password(account_id, password, ip=get_ip()):
        return ""

    if len(base64_decode(acc_comment)) > 140:
        return ""

    if not restric_reupload(usercomment_db, {"account_id": account_id}, "comment_id", "upload_time", 60):
        return ""

    comment_id = last_id(usercomment_db, "comment_id")

    sample_comment = {
        "comment_id": comment_id,
        "account_id": account_id,
        "comment": base64_encode(acc_comment),
        "like": 0,
        "upload_time": int(time()),
        "is_deleted": 0
    }

    usercomment_db.insert_one(sample_comment)

    return "1"

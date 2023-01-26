from utils import *
from config import *
from . import comment
from time import time
from flask import request


@comment.route(f"{Path.TO_DATABASE}/uploadGJComment21.php", methods=("POST", "GET"))
def upload_comment():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    level_comment = get_arg("comment")
    level_id = int_arg(get_arg("levelID"))
    percent = int_arg(get_arg("percent"))

    clear_comment = base64_decode(level_comment)

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    if len(clear_comment) > 140:
        return "-1"

    if not limit_check(percent, 100):
        return "-1"

    if level_db.count_documents({
        "level_id": level_id,
        "deleted": 0
    }) == 0:
        return "-1"

    if clear_comment[0] == "!":
        command(account_id, level_id, clear_comment)
        return "-1"

    if not restric_reupload(levelcomment_db, {"account_id": account_id}, "comment_id", "upload_time", 10):
        return "-1"

    comment_id = last_id(levelcomment_db, "comment_id")

    sample_comment = {
        "comment_id": comment_id,
        "account_id": account_id,
        "level_id": level_id,
        "comment": base64_encode(level_comment),
        "like": 0,
        "percent": percent,
        "upload_time": int(time()),
        "is_deleted": 0
    }

    levelcomment_db.insert_one(sample_comment)

    return "1"

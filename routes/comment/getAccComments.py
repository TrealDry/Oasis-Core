import pymongo
from utils import *
from config import *
from . import comment
from flask import request


@comment.route(f"{Path.TO_DATABASE}/getGJAccountComments20.php", methods=("POST", "GET"))
def get_account_comment():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))

    prefix = user_db.find_one({"account_id": account_id})["user_prefix"]
    prefix = prefix + " / " if prefix != "" else ""

    page = int_arg(get_arg('page'))
    offset = page * 10

    query = {
        "account_id": account_id,
        "is_deleted": 0
    }

    comments = tuple(usercomment_db.find(query).skip(offset).limit(10).sort([("comment_id", pymongo.DESCENDING)]))

    responce = ""

    for i in comments:
        single_responce = {
            2: base64_decode(i["comment"]), 4: i["like"],
            9: prefix + time_converter(i["upload_time"]),
            6: i["comment_id"]
        }

        responce += resp_proc(single_responce, 2) + "|"

    responce = responce[:-1] + f"#{usercomment_db.count_documents(query)}:{offset}:10"

    return responce

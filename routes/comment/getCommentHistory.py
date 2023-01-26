import pymongo
from utils import *
from config import *
from . import comment
from flask import request


@comment.route(f"{Path.TO_DATABASE}/getGJCommentHistory.php", methods=("POST", "GET"))
def get_comment_history():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    user_id = int_arg(get_arg("userID"))
    account_id = user_db.find_one({"user_id": user_id})["account_id"]

    page = int_arg(get_arg("page"))
    offset = page * 10

    mode = int_arg(get_arg("mode"))
    sort = [("comment_id", pymongo.DESCENDING)] if mode == 0 else [("like", pymongo.DESCENDING)]

    query = {
        "account_id": account_id,
        "is_deleted": 0
    }

    comments = tuple(levelcomment_db.find(query).skip(offset).limit(10).sort(sort))

    responce = ""

    for i in comments:
        user_info = tuple(user_db.find({"user_id": user_id}))

        prefix = user_info[0]["user_prefix"]
        prefix = prefix + " / " if prefix != "" else ""

        glow = user_info[0]["icon_glow"]
        glow = 2 if glow == 1 else glow

        single_comment_responce = {
            1: i["level_id"], 2: base64_decode(i["comment"]), 3: user_id, 4: i["like"], 7: 0,
            10: i["percent"], 9: prefix + time_converter(i["upload_time"]),
            6: i["comment_id"], 11: user_info[0]["mod_level"]
        }

        if user_info[0]["color_comment"] != "":
            single_comment_responce.update({12: user_info[0]["color_comment"]})

        responce += resp_proc(single_comment_responce, 2) + ":"

        single_user_responce = {
            1: user_info[0]["username"], 9: user_info[0]["icon_id"], 10: user_info[0]["first_color"],
            11: user_info[0]["second_color"], 14: user_info[0]["icon_type"], 15: glow, 16: account_id
        }

        responce += resp_proc(single_user_responce, 2) + "|"

    responce = responce[:-1] + f"#{levelcomment_db.count_documents(query)}:{offset}:10"

    return responce

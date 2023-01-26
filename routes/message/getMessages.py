import pymongo
from utils import *
from config import *
from . import message
from flask import request


@message.route(f"{Path.TO_DATABASE}/getGJMessages20.php", methods=("POST", "GET"))
def get_messages():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    page = int_arg(get_arg("page"))
    offset = page * 10

    type_message = int_arg(get_arg("getSent"))

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    query = {
        "is_deleted": 0
    }

    if type_message == 0:
        query["recipient_id"] = account_id
    elif type_message == 1:
        query["account_id"] = account_id
    else:
        return "-1"

    messages = tuple(message_db.find(query).skip(offset).limit(10).sort([("message_id", pymongo.DESCENDING)]))

    responce = ""

    for i in messages:
        is_read = i["is_read"] if type_message == 0 else 1

        if type_message == 0:
            query_user = {"account_id": i["account_id"]}
        else:
            query_user = {"account_id": i["recipient_id"]}

        user_info = tuple(user_db.find(query_user))

        prefix = user_info[0]["user_prefix"]
        prefix = prefix + " / " if prefix != "" else ""

        single_message = {
            6: user_info[0]["username"], 3: user_info[0]["user_id"],
            2: query_user["account_id"], 1: i["message_id"], 4: i["subject"],
            8: is_read, 9: type_message, 7: prefix + time_converter(i["upload_time"])
        }

        responce += resp_proc(single_message) + "|"

    responce = responce[:-1] + f"#{message_db.count_documents(query)}:{page * 50}:{page * 50 + 50}"

    return responce

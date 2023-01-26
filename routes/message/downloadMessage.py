from utils import *
from config import *
from . import message
from flask import request


@message.route(f"{Path.TO_DATABASE}/downloadGJMessage20.php", methods=("POST", "GET"))
def download_message():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    message_id = int_arg(get_arg("messageID"))

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    msg = tuple(message_db.find({
        "message_id": message_id,
        "is_deleted": 0
    }))

    try:
        if msg[0]["recipient_id"] == account_id:
            type_message = 0
            query_user = {"account_id": msg[0]["account_id"]}
        elif msg[0]["account_id"] == account_id:
            type_message = 1
            query_user = {"account_id": msg[0]["recipient_id"]}
        else:
            return "-1"
    except IndexError:
        return "-1"

    user_info = tuple(user_db.find(query_user))

    prefix = user_info[0]["user_prefix"]
    prefix = prefix + " / " if prefix != "" else ""

    is_read = msg[0]["is_read"] if type_message == 0 else 1

    if type_message == 0 and is_read == 0:
        message_db.update_one({"message_id": message_id}, {"$set": {
            "is_read": 1
        }})
        user_db.update_one({"account_id": account_id}, {"$inc": {
            "missed_messages": -1
        }})

    responce = {
        6: user_info[0]["username"], 3: user_info[0]["user_id"], 2: query_user["account_id"],
        1: message_id, 4: msg[0]["subject"], 8: is_read, 9: type_message, 5: msg[0]["body"],
        7: prefix + time_converter(msg[0]["upload_time"])
    }

    responce = resp_proc(responce)

    return responce

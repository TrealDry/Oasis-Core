from utils import *
from config import *
from . import message
from flask import request


@message.route(f"{Path.TO_DATABASE}/deleteGJMessages20.php", methods=("POST", "GET"))
def delete_message():
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
            query_user = {"account_id": msg[0]["account_id"]}
        elif msg[0]["account_id"] == account_id:
            query_user = {"account_id": msg[0]["recipient_id"]}
        else:
            return "-1"
    except IndexError:
        return "-1"

    if msg[0]["is_read"] == 0:
        user_db.update_one({"account_id": query_user["account_id"]}, {"$inc": {
            "missed_messages": -1
        }})

    message_db.update_one({"message_id": message_id}, {"$set": {
        "is_deleted": 1
    }})

    return "1"

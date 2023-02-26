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
    message_ids = None

    try:
        message_ids = get_arg("messages").split(",")
    except AttributeError:
        if message_id is None:
            return "-1"

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    if message_ids is None:
        msg = tuple(message_db.find({
            "message_id": message_id,
            "is_deleted": 0
        }))
    else:
        query = {
            "is_deleted": 0,
            "$or": []
        }

        try:
            for i in message_ids:
                query["$or"].append({"message_id": int(i)})
        except ValueError:
            return "-1"

        msg = message_db.find(query)
        msg = tuple(msg)

    for i in msg:
        try:
            if i["recipient_id"] == account_id:
                query_user = {"account_id": i["account_id"]}
            elif i["account_id"] == account_id:
                query_user = {"account_id": i["recipient_id"]}
            else:
                return "-1"
        except IndexError:
            return "-1"

        if i["is_read"] == 0:
            user_db.update_one({"account_id": query_user["account_id"]}, {"$inc": {
                "missed_messages": -1
            }})

        message_db.update_one({"message_id": i["message_id"]}, {"$set": {
            "is_deleted": 1
        }})

    return "1"

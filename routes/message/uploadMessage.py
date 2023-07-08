from utils import *
from config import *
from . import message
from time import time
from flask import request


@message.route(f"{Path.TO_DATABASE}/uploadGJMessage20.php", methods=("POST", "GET"))
def upload_message():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    recipient_id = int_arg(get_arg("toAccountID"))

    subject = get_arg("subject")
    body = get_arg("body")

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    if not limit_check(len(base64_decode(subject)), 35) or \
       not limit_check(len(xor_cipher(base64_decode(body), "14251")), 200):
        return "-1"

    if account_id == recipient_id:
        return "-1"

    if not restric_reupload(message_db, {"account_id": account_id}, "message_id", "upload_time", 30):
        return "-1"

    if blocklist_db.count_documents({"$or": [
        {"account_id": account_id, "account_id_2": recipient_id},
        {"account_id": recipient_id, "account_id_2": account_id}
    ]}) == 1:
        return "-1"

    if user_db.find_one({"account_id": recipient_id})["message_state"] == 1:
        if friendship_db.count_documents({"$or": [
            {"account_id": account_id, "account_id_2": recipient_id},
            {"account_id": recipient_id, "account_id_2": account_id}
        ]}) == 0:
            return "-1"

    if user_db.find_one({"account_id": recipient_id})["message_state"] == 2:
        return "-1"

    message_db.insert_one({
        "message_id": last_id(message_db, "message_id"),
        "account_id": account_id,
        "recipient_id": recipient_id,
        "subject": subject,
        "body": body,
        "upload_time": int(time()),
        "is_read": 0,
        "is_deleted": 0
    })

    user_db.update_one({"account_id": recipient_id}, {"$inc": {
        "missed_messages": 1
    }})

    return "1"

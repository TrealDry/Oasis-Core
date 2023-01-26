from utils import *
from config import *
from time import time
from flask import request
from . import relationship


@relationship.route(f"{Path.TO_DATABASE}/uploadFriendRequest20.php", methods=("POST", "GET"))
def upload_friend_request():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    recipient_id = int_arg(get_arg("toAccountID"))
    comment = get_arg("comment")

    comment = "" if comment == "0" else comment

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    if not limit_check(len(base64_decode(comment)), 140):
        return "-1"

    if account_id == recipient_id:
        return "-1"

    if friendreq_db.count_documents({"$or": [
        {"account_id": account_id, "recipient_id": recipient_id},
        {"account_id": recipient_id, "recipient_id": account_id}
    ]}) == 1:
        return "-1"

    if friendship_db.count_documents({"$or": [
        {"account_id": account_id, "account_id_2": recipient_id},
        {"account_id": recipient_id, "account_id_2": account_id}
    ]}) == 1:
        return "-1"

    if blocklist_db.count_documents({"$or": [
        {"account_id": account_id, "account_id_2": recipient_id},
        {"account_id": recipient_id, "account_id_2": account_id}
    ]}) == 1:
        return "-1"

    if user_db.find_one({"account_id": recipient_id})["friends_state"] == 1:
        return "-1"

    friendreq_db.insert_one({
        "req_id": last_id(friendreq_db, "req_id"),
        "account_id": account_id,
        "recipient_id": recipient_id,
        "comment": comment,
        "timestamp": int(time())
    })

    user_db.update_one({"account_id": recipient_id}, {"$inc": {
        "friend_requests": 1
    }})

    return "1"

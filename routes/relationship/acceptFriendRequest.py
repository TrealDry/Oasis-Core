from utils import *
from config import *
from flask import request
from . import relationship


@relationship.route(f"{Path.TO_DATABASE}/acceptGJFriendRequest20.php", methods=("POST", "GET"))
def accept_friend_request():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    sender_id = int_arg(get_arg("targetAccountID"))
    request_id = int_arg(get_arg("requestID"))

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    if friendreq_db.count_documents({
        "req_id": request_id,
        "account_id": sender_id,
        "recipient_id": account_id
    }) == 0:
        return "-1"

    user_db.update_one({"account_id": account_id}, {"$inc": {
        "friend_requests": -1
    }})

    friendship_db.insert_one({
        "account_id": sender_id,
        "account_id_2": account_id
    })

    friendreq_db.delete_one({
        "req_id": request_id
    })

    return "1"

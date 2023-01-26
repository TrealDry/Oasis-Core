from utils import *
from config import *
from flask import request
from . import relationship


@relationship.route(f"{Path.TO_DATABASE}/deleteGJFriendRequests20.php", methods=("POST", "GET"))
def delete_friend_request():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    target_account_id = int_arg(get_arg("targetAccountID"))
    is_sender = int_arg(get_arg("isSender"))

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    if is_sender == 0:
        query = {
            "account_id": target_account_id,
            "recipient_id": account_id
        }
    elif is_sender == 1:
        query = {
            "account_id": account_id,
            "recipient_id": target_account_id
        }
    else:
        return "-1"

    if friendreq_db.count_documents(query) == 0:
        return "-1"

    user_db.update_one({"account_id": query["recipient_id"]}, {"$inc": {
        "friend_requests": -1
    }})

    friendreq_db.delete_one(query)

    return "1"

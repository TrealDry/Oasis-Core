from utils import *
from config import *
from flask import request
from . import relationship


@relationship.route(f"{Path.TO_DATABASE}/blockGJUser20.php", methods=("POST", "GET"))
def block_user():
    if not secret_check(request.values.get("secret"), 2):
        return "1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    target_account_id = int_arg(get_arg("targetAccountID"))

    if not check_password(account_id, password, ip=get_ip()):
        return "1"

    if account_id == target_account_id:
        return "1"

    query = {"$or": [
        {"account_id": account_id, "account_id_2": target_account_id},
        {"account_id": target_account_id, "account_id_2": account_id}
    ]}

    query_two = {"$or": [
        {"account_id": account_id, "recipient_id": target_account_id},
        {"account_id": target_account_id, "recipient_id": account_id}
    ]}

    if blocklist_db.count_documents(query) == 1:
        return "1"

    if friendship_db.count_documents(query) == 1:
        friendship_db.delete_one(query)

    if friendreq_db.count_documents({
        "account_id": account_id, "recipient_id": target_account_id
    }) == 1:
        friendreq_db.delete_one(query_two)
        user_db.update_one({"recipient_id": target_account_id}, {"$inc": {
            "friend_requests": -1
        }})
    elif friendreq_db.count_documents({
        "account_id": target_account_id, "recipient_id": account_id
    }) == 1:
        friendreq_db.delete_one(query_two)
        user_db.update_one({"recipient_id": account_id}, {"$inc": {
            "friend_requests": -1
        }})

    message_db.update_many(query_two, {"$set": {
        "is_deleted": 1
    }})

    blocklist_db.insert_one({
        "account_id": account_id, "account_id_2": target_account_id
    })

    return "1"

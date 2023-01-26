from utils import *
from config import *
from flask import request
from . import relationship


@relationship.route(f"{Path.TO_DATABASE}/removeGJFriend20.php", methods=("POST", "GET"))
def remove_friend():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    target_account_id = int_arg(get_arg("targetAccountID"))

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    query = {"$or": [
        {"account_id": account_id, "account_id_2": target_account_id},
        {"account_id": target_account_id, "account_id_2": account_id}
    ]}

    if friendship_db.count_documents(query) == 0:
        return "-1"

    friendship_db.delete_one(query)

    return "1"

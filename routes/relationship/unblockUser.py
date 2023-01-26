from utils import *
from config import *
from flask import request
from . import relationship


@relationship.route(f"{Path.TO_DATABASE}/unblockGJUser20.php", methods=("POST", "GET"))
def unblock_user():
    if not secret_check(request.values.get("secret"), 2):
        return "1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    target_account_id = int_arg(get_arg("targetAccountID"))

    if not check_password(account_id, password, ip=get_ip()):
        return "1"

    if account_id == target_account_id:
        return "1"

    if blocklist_db.count_documents({"$or": [
        {"account_id": account_id, "account_id_2": target_account_id},
        {"account_id": target_account_id, "account_id_2": account_id}
    ]}) == 0:
        return "1"

    blocklist_db.delete_one({
        "account_id": account_id, "account_id_2": target_account_id
    })

    return "1"

from . import misc
from utils import *
from config import *
from time import time
from flask import request


@misc.route(f"{Path.TO_DATABASE}/likeGJItem211.php", methods=("POST", "GET"))
def like_item():
    if not secret_check(request.values.get("secret"), 2):
        return ""

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    item_id = int_arg(get_arg("itemID"))
    type_comment = int_arg(get_arg("type"))
    like = 1 if int_arg(get_arg("like")) != 0 else -1

    if not check_password(account_id, password, ip=get_ip()):
        return ""

    if actionlike_db.count_documents({
        "item_id": item_id,
        "type_comment": type_comment,
        "account_id": account_id
    }) == 1:
        return ""

    try:
        if type_comment == 1:  # Уровень
            level_db.update_one({"level_id": item_id}, {"$inc": {"like": like}})
        elif type_comment == 2:  # Комментарий к уровню
            levelcomment_db.update_one({"comment_id": item_id}, {"$inc": {"like": like}})
        elif type_comment == 3:  # Комментарий на аккаунте
            usercomment_db.update_one({"comment_id": item_id}, {"$inc": {"like": like}})
        else:
            return ""

        actionlike_db.insert_one({
            "item_id": item_id,
            "type_comment": type_comment,
            "like": like,
            "account_id": account_id,
            "timestamp": int(time())
        })

        return "1"
    except:
        return ""

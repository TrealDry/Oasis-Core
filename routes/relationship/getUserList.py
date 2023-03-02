import operator
from utils import *
from config import *
from flask import request
from . import relationship


@relationship.route(f"{Path.TO_DATABASE}/getGJUserList20.php", methods=("POST", "GET"))
def get_user_list():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    user_type = int_arg(get_arg("type"))

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    query = {
        "$or": [
            {"account_id": account_id},
            {"account_id_2": account_id}
        ]
    }

    if user_type == 0:  # Друзья
        users = tuple(friendship_db.find(query))
    elif user_type == 1:  # Блок лист
        users = tuple(blocklist_db.find(query))
    else:
        return "-1"

    responce = ""
    responce_arr = []

    for i in users:
        if i["account_id"] != account_id:
            user_query = {"account_id": i["account_id"]}
        else:
            user_query = {"account_id": i["account_id_2"]}

        user_info = tuple(user_db.find(user_query))

        responce_arr.append({
            1: user_info[0]["username"], 2: user_info[0]["user_id"], 9: user_info[0]["icon_id"],
            10: user_info[0]["first_color"], 11: user_info[0]["second_color"], 14: user_info[0]["icon_type"],
            15: 0, 16: user_info[0]["account_id"], 18: user_info[0]["message_state"], 41: ""
        })

    responce_arr.sort(reverse=True, key=operator.itemgetter(1))

    for i in responce_arr:
        responce += resp_proc(i) + "|"

    if responce != "":
        responce = responce[:-1]
        return responce
    else:
        return "-2"

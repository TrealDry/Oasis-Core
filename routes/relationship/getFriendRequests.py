import pymongo
from utils import *
from config import *
from flask import request
from . import relationship


@relationship.route(f"{Path.TO_DATABASE}/getGJFriendRequests20.php", methods=("POST", "GET"))
def get_friend_requests():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    page = int_arg(get_arg("page"))
    offset = page * 10

    type_message = int_arg(get_arg("getSent"))

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    query = {}

    if type_message == 0:
        query["recipient_id"] = account_id
    elif type_message == 1:
        query["account_id"] = account_id
    else:
        return "-1"

    friendreqs = tuple(friendreq_db.find(query).skip(offset).limit(10).sort([("req_id", pymongo.DESCENDING)]))

    responce = ""

    for i in friendreqs:
        if type_message == 0:
            query_user = {"account_id": i["account_id"]}
        else:
            query_user = {"account_id": i["recipient_id"]}

        user_info = tuple(user_db.find(query_user))

        glow = user_info[0]["icon_glow"]
        glow = 2 if glow == 1 else glow

        single_friendreq = {
            1: user_info[0]["username"], 2: user_info[0]["user_id"], 9: user_info[0]["icon_id"],
            10: user_info[0]["first_color"], 11: user_info[0]["second_color"], 14: user_info[0]["icon_type"],
            15: glow, 16: user_info[0]["account_id"], 32: i["req_id"], 35: i["comment"], 41: 1,
            37: time_converter(i["timestamp"])
        }

        responce += resp_proc(single_friendreq) + "|"

    responce = responce[:-1] + f"#:{page * 20}:20"

    return responce

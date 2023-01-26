import pymongo
from . import score
from utils import *
from config import *
from flask import request


@score.route(f"{Path.TO_DATABASE}/getGJScores20.php", methods=("POST", "GET"))
def get_scores():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    type_score = get_arg("type")

    if type_score == "0":
        type_score = "top"

    query = {"is_top_banned": 0}
    limit = 50
    sort = [("star", pymongo.DESCENDING)]

    if type_score == "top" or \
       type_score == "relative":
        query["star"] = {"$gte": 10}

    elif type_score == "friends":
        query["$or"] = [{"account_id": account_id}]

        all_friend = tuple(friendship_db.find({"$or": [
            {"account_id": account_id}, {"account_id_2": account_id}
        ]}))
        for i in all_friend:
            if i["account_id"] != account_id:
                acc_id = i["account_id"]
            else:
                acc_id = i["account_id_2"]
            query["$or"].append({
                "account_id": acc_id
            })

    elif type_score == "creators":
        query["creator_point"] = {"$gt": 0}
        sort = [("creator_point", pymongo.DESCENDING)]

    else:
        return "-1"

    responce = ""

    users = user_db.find(query).limit(limit)

    if sort:
        users.sort(sort)

    counter = 1

    for i in users:
        single_user = {
            1: i["username"], 2: i["user_id"], 13: i["secret_coin"], 17: i["user_coin"],
            6: counter, 9: i["icon_id"], 10: i["first_color"], 11: i["second_color"], 14: i["icon_type"],
            15: 0, 16: i["account_id"], 3: i["star"], 8: i["creator_point"], 46: i["diamond"], 4: i["demon"]
        }

        counter += 1

        responce += resp_proc(single_user) + "|"

    return responce

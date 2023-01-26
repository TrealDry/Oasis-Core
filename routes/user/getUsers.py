from . import user
from utils import *
from config import Path


@user.route(f"{Path.TO_DATABASE}/getGJUsers20.php", methods=("POST", "GET"))
def get_users():
    if not secret_check(get_arg("secret"), 2):
        return "-1"

    search = get_arg("str")

    page = int_arg(get_arg("page"))
    offset = page * 10

    query = {
        "username": {"$regex": f"(?i)^{search}"}
    }

    if user_db.count_documents(query) == 0:
        return "-1"

    users = tuple(user_db.find(query).skip(offset).limit(10))

    responce = ""

    for i in users:
        single_user = {
            1: i["username"], 2: i["user_id"], 13: i["secret_coin"], 17: i["user_coin"], 6: "", 9: i["icon_id"],
            10: i["first_color"], 11: i["second_color"], 14: i["icon_type"], 15: 0, 16: i["account_id"], 3: i["star"],
            8: i["creator_point"], 4: ["demon"]
        }

        responce += resp_proc(single_user) + "|"

    responce = responce[:-1] + f"#{user_db.count_documents(query)}:{offset}:10"

    return responce

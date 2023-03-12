from . import level
from utils import *
from config import *
from flask import request, abort


@level.route(f"{Path.TO_DATABASE}/suggestGJStars.php", methods=("POST", "GET"))
@level.route(f"{Path.TO_DATABASE}/suggestGJStars20.php", methods=("POST", "GET"))
def suggest_stars():
    if not secret_check(request.values.get("secret"), 4):
        abort(500)

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    level_id = int_arg(get_arg("levelID"))

    star = int_arg(get_arg("stars"))
    is_featured = int_arg(get_arg("feature"))

    if not check_password(account_id, password, ip=get_ip()):
        abort(500)

    if roleassing_db.count_documents({
        "account_id": account_id
    }) == 0:
        return "-2"

    if level_db.count_documents({
        "level_id": level_id,
        "deleted": 0
    }) == 0:
        abort(500)

    role = tuple(role_db.find({"role_id": roleassing_db.find_one({"account_id": account_id})["role_id"]}))
    query_level = {}

    if role[0]["mod_button_type"] == 1:
        suggest_db.insert_one({
            "account_id": account_id,
            "level_id": level_id,
            "stars": star,
            "featured": is_featured,
            "time": time()
        })
        return "1"
    elif role[0]["mod_button_type"] == 2:
        query_level["featured"] = 1 if is_featured else 0

        if star == 1:
            query_level.update({
                "auto": 1,
                "star": 1,
                "demon": 0,
                "demon_type": 0,
                "difficulty": 1,
            })
        elif star == 10:
            query_level.update({
                "auto": 0,
                "star": 10,
                "demon": 1,
                "demon_type": 3,
                "difficulty": 5
            })
        elif 1 < star < 10:
            query_level.update({
                "auto": 0,
                "star": star,
                "demon": 0,
                "demon_type": 0,
                "difficulty": diff_type_conv(star)
            })
        else:
            abort(500)
    else:
        return "1"

    if query_level:
        level_db.update_one({"level_id": level_id}, {"$set": query_level})

    return "1"

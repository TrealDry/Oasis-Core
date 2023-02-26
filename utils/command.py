from time import time
from config import Path
from utils import database as db


def command(account_id, level_id, comment):
    query_acc = {
        "account_id": account_id
    }

    if db.roleassing_db.count_documents(query_acc) == 0:
        return False

    role = tuple(db.role_db.find({"role_id": db.roleassing_db.find_one(query_acc)["role_id"]}))
    comment_arr = comment.split(" ")

    query_level = {}

    if comment == "!delete" and role[0]["command_delete"] == 1:
        with open(f"{Path.TO_ROOT}/data/level/{str(level_id)}.level", "w") as level_file:
            level_file.write("")

        query_level = {"deleted": 1}
        db.levelcomment_db.update_many({"level_id": level_id}, {"$set": {
            "is_deleted": 1
        }})

    elif comment == "!featured" and role[0]["command_featured"] == 1:
        query_level = {"featured": 1}

    elif comment == "!unfeatured" and role[0]["command_featured"] == 1:
        query_level = {"featured": 0}

    elif comment == "!epic" and role[0]["command_epic"] == 1:
        query_level = {"featured": 1, "epic": 1}

    elif comment == "!unepic" and role[0]["command_epic"] == 1:
        query_level = {"epic": 0}

    elif comment == "!verifycoins" and role[0]["command_verifycoins"] == 1:
        query_level = {"silver_coin": 1}

    elif comment == "!unverifycoins" and role[0]["command_verifycoins"] == 1:
        query_level = {"silver_coin": 0}

    elif comment_arr[0] == "!pass" and role[0]["command_pass"] == 1:
        try:
            query_level = {"level_password": int(comment_arr[1])}
        except IndexError:
            return False
        except ValueError:
            return False

    elif comment_arr[0] == "!rate" and role[0]["command_rate"] == 1:
        try:
            if len(comment_arr) == 2:
                query_level = {
                    "difficulty": int(comment_arr[1]),
                }
            elif len(comment_arr) == 3:
                query_level = {
                    "difficulty": int(comment_arr[1]),
                    "star": int(comment_arr[2]),
                    "rate_date": int(time())
                }
        except ValueError:
            return False

    elif comment == "!unrate" and role[0]["command_rate"] == 1:
        query_level = {
            "difficulty": 0,
            "star": 0,
            "featured": 0,
            "epic": 0,
            "silver_coin": 0,
            "auto": 0,
            "demon": 0,
            "demon_type": 0,
            "rate_date": 0
        }

    elif comment == "!demon" and role[0]["command_demon"] == 1:
        query_level = {"demon": 1, "difficulty": 5, "demon_type": 3}

    elif comment == "!undemon" and role[0]["command_demon"] == 1:
        query_level = {"demon": 0, "demon_type": 0}

    elif comment_arr[0] == "!song" and role[0]["command_song"] == 1:
        try:
            query_level = {"non_official_song": int(comment_arr[1])}
        except IndexError:
            return False
        except ValueError:
            return False

    elif comment_arr[0] == "!rename" and role[0]["command_rename"] == 1:
        level_name = ""
        try:
            for i in range(len(comment_arr) - 1):
                level_name += comment_arr[i + 1] + " "
            query_level = {"level_name": level_name[:-1]}
        except IndexError:
            return False

    elif comment_arr[0] == "!setacc" and role[0]["command_setacc"] == 1:
        try:
            user_info = tuple(db.user_db.find({"username": {"$regex": f"^{comment_arr[1]}$", '$options': 'i'}}))
            query_level = {
                "account_id": user_info[0]["account_id"],
                "user_id": user_info[0]["user_id"],
                "username": user_info[0]["username"]
            }
        except IndexError:
            return False

    if query_level:
        db.level_db.update_one({"level_id": level_id}, {"$set": query_level})
        return True

    return False

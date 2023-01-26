from utils import *
from config import *
from . import levelpack
from flask import request


@levelpack.route(f"{Path.TO_DATABASE}/getGJGauntlets21.php", methods=("POST", "GET"))
def get_gauntlets():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    gauntlets = tuple(gauntlet_db.find())

    responce = ""
    hash_string = ""

    for i in gauntlets:
        single_gauntlet = {
            1: i["gauntlet_id"], 3: i["level"]
        }

        hash_string += f"{i['gauntlet_id']}{i['level']}"
        responce += resp_proc(single_gauntlet) + "|"

    responce = responce[:-1] + f"#{return_hash(hash_string)}"

    return responce

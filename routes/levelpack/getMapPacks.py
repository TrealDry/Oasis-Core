import pymongo
from utils import *
from config import *
from . import levelpack
from flask import request


@levelpack.route(f"{Path.TO_DATABASE}/getGJMapPacks21.php", methods=("POST", "GET"))
def get_map_packs():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    page = int_arg(get_arg('page'))
    offset = page * 10

    responce = ""
    hash_string = ""

    mappacks = tuple(mappack_db.find().skip(offset).limit(10).sort([("pack_id", pymongo.ASCENDING)]))

    for i in mappacks:
        single_pack = {
            1: i["pack_id"], 2: i["pack_name"], 3: i["level"], 4: i["star"], 5: i["coin"],
            6: i["difficulty"], 7: i["text_color"], 8: i["bar_color"]
        }

        responce += resp_proc(single_pack) + "|"
        hash_string += f"{str(i['pack_id'])[0]}{str(i['pack_id'])[-1]}{i['star']}{i['coin']}"

    responce = responce[:-1] + f"#{mappack_db.count_documents({})}:{offset}:10#{return_hash(hash_string)}"

    return responce

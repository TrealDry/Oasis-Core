import pymongo
from . import level
from utils import *
from config import *
from time import time
from flask import request


@level.route(f"{Path.TO_DATABASE}/getGJDailyLevel.php", methods=("POST", "GET"))
def get_daily_level():
    if not secret_check(request.values.get("secret"), 2):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    if check_password(account_id, password, ip=get_ip()):
        pass

    time_now = int(time())

    type_daily = int_arg(get_arg("weekly"))

    additional_id = 0 if type_daily == 0 else 100001
    time_limit = 86400 if type_daily == 0 else 604800

    daily_level = tuple(dailylevel_db.find({
        "timestamp": {"$lte": time_now - 1},
        "daily_type": type_daily
    }).sort([("timestamp", pymongo.DESCENDING)]).limit(1))

    try:
        return f"{daily_level[0]['daily_id'] + additional_id}|{(daily_level[0]['timestamp'] + time_limit) - time_now}"
    except IndexError:
        return "-1"

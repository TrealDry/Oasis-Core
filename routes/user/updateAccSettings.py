from . import user
from utils import *
from config import Path


@user.route(f"{Path.TO_DATABASE}/updateGJAccSettings20.php", methods=("POST", "GET"))
def update_acc_settings():
    if not secret_check(get_arg("secret"), 1):
        return "-1"

    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    message = int_arg(get_arg("mS"))
    friend = int_arg(get_arg("frS"))
    comment = int_arg(get_arg("cS"))

    youtube = get_arg("yt")
    twitter = get_arg("twitter")
    twitch = get_arg("twitch")

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    if not limit_check(message, 2) or not limit_check(friend, 1) or \
       not limit_check(comment, 2):
        return "-1"

    user_db.update_one({"account_id": account_id}, {"$set": {
        "message_state": message,
        "friends_state": friend,
        "comment_history_state": comment,
        "youtube": youtube,
        "twitter": twitter,
        "twitch": twitch
    }})

    return "1"

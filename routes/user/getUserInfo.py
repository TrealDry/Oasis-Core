from . import user
from utils import *
from config import Path


@user.route(f"{Path.TO_DATABASE}/getGJUserInfo20.php", methods=("POST", "GET"))
def get_user_info():
    if not secret_check(get_arg("secret"), 2):
        return "-1"

    target_acc_id = int_arg(get_arg("targetAccountID"))
    account_id = int_arg(get_arg("accountID"))
    password = get_arg("gjp")

    is_account_owner = False

    # Если аккаунта не существует
    if user_db.count_documents({"account_id": target_acc_id}) == 0:
        return "-1"

    tg_user = tuple(user_db.find({"account_id": target_acc_id}))

    response = {
        1: tg_user[0]["username"], 2: tg_user[0]["user_id"], 13: tg_user[0]["secret_coin"], 17: tg_user[0]["user_coin"],
        10: tg_user[0]["first_color"], 11: tg_user[0]["second_color"], 3: tg_user[0]["star"], 46: tg_user[0]["diamond"],
        4: tg_user[0]["demon"], 8: tg_user[0]["creator_point"], 18: tg_user[0]["message_state"],
        19: tg_user[0]["friends_state"], 50: tg_user[0]["comment_history_state"], 20: tg_user[0]["youtube"],
        21: tg_user[0]["icon_cube"], 22: tg_user[0]["icon_ship"], 23: tg_user[0]["icon_ball"],
        24: tg_user[0]["icon_ufo"], 25: tg_user[0]["icon_wave"], 26: tg_user[0]["icon_robot"],
        28: tg_user[0]["icon_glow"], 43: tg_user[0]["icon_spider"], 48: 0, 30: 0, 16: target_acc_id
    }

    if account_id != 0:
        if check_password(account_id, password, ip=get_ip()):
            is_account_owner = True

    if is_account_owner:
        if friendship_db.count_documents({"$or": [
            {"account_id": account_id, "account_id_2": target_acc_id},
            {"account_id": target_acc_id, "account_id_2": account_id}
        ]}) == 1:
            response.update({31: 1})
        elif friendreq_db.count_documents({
            "account_id": account_id, "recipient_id": target_acc_id
        }) == 1:
            response.update({31: 4})
        elif friendreq_db.count_documents({
            "account_id": target_acc_id, "recipient_id": account_id
        }) == 1:
            response.update({31: 3})
        else:
            response.update({31: 0})

    response.update({44: tg_user[0]["twitter"], 45: tg_user[0]["twitch"], 49: tg_user[0]["mod_level"]})

    if account_id == target_acc_id and is_account_owner:
        response.update({38: tg_user[0]["missed_messages"], 39: tg_user[0]["friend_requests"], 40: 0})

    response.update({29: 1})

    return resp_proc(response)

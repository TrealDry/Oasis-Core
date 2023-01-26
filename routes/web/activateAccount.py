from . import web
from utils import *
from config import Security
from flask import render_template


@web.route("/activate_account", methods=("POST", "GET"))
def activate_account():
    code = int_arg(get_arg_web("code"))
    password = get_arg_form("password")

    message = ""

    if code == 0 or account_db.count_documents({"confirmation_code": code}) == 0:
        return "Account activation link is invalid!"

    if password is not None:
        account_id = account_db.find_one({"confirmation_code": code})["account_id"]

        if not hcaptcha.verify():
            message = "Captcha failed!"
        else:
            if check_password(account_id, password, False, False):
                user_id = last_id(user_db, "user_id")

                single_user = {"username": account_db.find_one({"account_id": account_id})["username"],
                               "user_id": user_id, "account_id": account_id, "star": 0, "demon": 0, "diamond": 0,
                               "user_coin": 0, "secret_coin": 0, "creator_point": 0, "first_color": 0,
                               "second_color": 3, "icon_id": 0, "icon_type": 0, "icon_cube": 0, "icon_ship": 0,
                               "icon_ball": 0, "icon_ufo": 0, "icon_wave": 0, "icon_robot": 0, "icon_spider": 0,
                               "icon_glow": 0, "missed_messages": 0, "friend_requests": 0, "ip": get_ip(),
                               "last_activity": 0, "is_banned": 0, "is_top_banned": 0, "user_prefix": "",
                               "mod_level": 0, "youtube": "", "twitter": "", "twitch": "", "message_state": 0,
                               "friends_state": 0, "comment_history_state": 0, "color_comment": "", "custom_color": 0,
                               "is_song_file_ban": 0, "is_song_link_ban": 0, "vip_status": 0}

                user_db.insert_one(single_user)
                account_db.update_one({"account_id": account_id}, {"$set": {
                    "confirmation_code": 0,
                    "user_id": user_id,
                    "valid": 1
                }})

                return "Your account has been verified!"

            message = "Password is invalid!"

    return render_template('activate_account.html', SITE_KEY=Security.SITE_KEY, message=message)

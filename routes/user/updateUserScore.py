from . import user
from utils import *
from config import Path


@user.route(f"{Path.TO_DATABASE}/updateGJUserScore22.php", methods=("POST", "GET"))
def update_user_score():
    account_id = int_arg(get_arg("accountID"))
    password = get_arg('gjp')

    star = int_arg(get_arg('stars'))
    demon = int_arg(get_arg('demons'))
    diamond = int_arg(get_arg('diamonds'))
    user_coin = int_arg(get_arg('userCoins'))
    secret_coin = int_arg(get_arg('coins'))

    if not check_password(account_id, password, ip=get_ip()):
        return "-1"

    if limit_check(star, 5000) and limit_check(demon, 100) and \
       limit_check(diamond, 999999999) and limit_check(user_coin, 200) and \
       limit_check(secret_coin, 100):
        user_db.update_one({"account_id": account_id}, {"$set": {
            "star": star,
            "demon": demon,
            "diamond": diamond,
            "user_coin": user_coin,
            "secret_coin": secret_coin,
            "icon_type": int_arg(get_arg('iconType')),
            "icon_id": int_arg(get_arg('icon')),
            "icon_cube": int_arg(get_arg('accIcon')),
            "icon_ship": int_arg(get_arg('accShip')),
            "icon_ball": int_arg(get_arg('accBall')),
            "icon_ufo": int_arg(get_arg('accBird')),
            "icon_wave": int_arg(get_arg('accDart')),
            "icon_robot": int_arg(get_arg('accRobot')),
            "icon_spider": int_arg(get_arg('accSpider')),
            "icon_glow": int_arg(get_arg('accGlow')),
            "first_color": int_arg(get_arg('color1')),
            "second_color": int_arg(get_arg('color2'))
        }})

        return str(user_db.find_one({"account_id": account_id})["user_id"])

    return "-1"

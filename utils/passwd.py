import bcrypt
from time import time
from utils import xor, database, base64_dec_enc


def decoding_gjp(x): return xor.xor_cipher(base64_dec_enc.base64_decode(x), "37526")


def hash_password(x): return bcrypt.hashpw(x.encode(), bcrypt.gensalt()).decode('ascii')


def check_password(account_id, password, gjp=True, isCheckValid=True, ip=""):
    if account_id == 0:
        return False

    if len(password) > 256:
        return False

    if database.user_db.count_documents({"account_id": account_id, "is_banned": 1}) == 1:
        return False

    if isCheckValid:
        try:
            if database.account_db.count_documents({"account_id": account_id, "valid": 0}) == 1:
                return False
        except TypeError:
            return False

        current_ip = database.user_db.find_one({"account_id": account_id})["ip"]

        if ip != current_ip and ip != "":
            database.user_db.update_one({"account_id": account_id}, {"$set": {
                "ip": ip
            }})

        database.user_db.update_one({"account_id": account_id}, {"$set": {
            "last_activity": int(time())
        }})

    if gjp:
        password = decoding_gjp(password)

    return bcrypt.checkpw(password.encode(),
                          database.account_db.find_one({"account_id": account_id})["password"].encode())

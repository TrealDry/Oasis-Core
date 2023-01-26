from config import Database
from pymongo import MongoClient

db = MongoClient(Database.URI)
current_db = db[Database.NAME]

actiondownload_db = current_db["actiondownload"]
levelcomment_db = current_db["levelcomment"]
usercomment_db = current_db["usercomment"]
suggest_db = current_db["suggestedlevel"]
dailylevel_db = current_db["dailylevel"]
roleassing_db = current_db["roleassing"]
friendship_db = current_db["friendship"]
actionlike_db = current_db["actionlike"]
masterkey_db = current_db["masterkey"]
friendreq_db = current_db["friendreq"]
blocklist_db = current_db["blocklist"]
bannedip_db = current_db["bannedip"]
gauntlet_db = current_db["gauntlet"]
mappack_db = current_db["mappack"]
account_db = current_db["account"]
message_db = current_db["message"]
level_db = current_db["level"]
user_db = current_db["user"]
song_db = current_db["song"]
role_db = current_db["role"]

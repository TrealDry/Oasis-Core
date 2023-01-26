from . import misc
from config import Path


@misc.route(f"{Path.TO_DATABASE}/getAccountURL.php", methods=("POST", "GET"))
def get_account_uri():
    return Path.TO_BACKUP

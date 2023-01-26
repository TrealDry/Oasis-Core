types_secrets = {
    1: "Wmfv3899gc9",
    2: "Wmfd2893gb7",
    3: "Wmfv2898gc9",
    4: "Wmfp3879gc3"
}


char_clear_regex = r"[^A-Za-z0-9]"


def secret_check(secret: str, type_secret: int):
    if secret == types_secrets[type_secret]:
        return True
    return False


def limit_check(value, limit):
    if 0 > value or value > limit:
        return False
    return True

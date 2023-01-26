import re


char_clear_regex = r"[^A-Za-z0-9 _=-]"


def char_clear(value):
    return re.sub(char_clear_regex, "", value, count=0)

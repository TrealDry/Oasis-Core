import time


def time_converter(timestamp):  # %02d
    time_now = int(time.time())
    time_interval = time_now - timestamp

    responce = ""

    if time_interval <= 59:
        responce = f"{time_interval} second"
        if time_interval > 1:
            responce += "s"
    elif 60 <= time_interval < 3600:
        responce = f"{time_interval // 60} minute"
        if time_interval > 120:
            responce += "s"
    elif 3600 <= time_interval < 86400:
        responce = f"{time_interval // 3600} hour"
        if time_interval > 7200:
            responce += "s"
    elif 86400 <= time_interval < 604800:
        responce = f"{time_interval // 86400} day"
        if time_interval > 172800:
            responce += "s"
    elif 604800 <= time_interval < 2629743:
        responce = f"{time_interval // 604800} week"
        if time_interval > 1209600:
            responce += "s"
    elif 2629743 <= time_interval < 31556926:
        responce = f"{time_interval // 2629743} month"
        if time_interval > 5259486:
            responce += "s"
    elif time_interval >= 31556926:
        responce = f"{time_interval // 31556926} year"
        if time_interval > 63113852:
            responce += "s"

    return responce

from time import time


def restric_reupload(coll, query, type_id, date, limit_time):
    try:
        last_loaded = tuple(coll.find(query).sort(type_id, -1).limit(1))

        if last_loaded is not None and \
           int(time()) - last_loaded[0][date] < limit_time:
            return False
        return True
    except IndexError:
        return True

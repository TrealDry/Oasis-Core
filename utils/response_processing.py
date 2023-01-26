def resp_proc(resp_dict, type=1):
    response_string = ""

    if type == 1:
        for key, value in resp_dict.items():
            response_string += f"{str(key)}:{str(value)}:"
    elif type == 2:
        for key, value in resp_dict.items():
            response_string += f"{str(key)}~{str(value)}~"
    elif type == 3:
        for key, value in resp_dict.items():
            response_string += f"{str(key)}~|~{str(value)}~|~"

    return response_string[:-1]

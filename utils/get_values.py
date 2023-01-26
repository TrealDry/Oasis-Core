from flask import request


def bool_str(x): return x == '1'
def get_arg_web(x): return request.args.get(x)
def get_arg_form(x): return request.form.get(x)
def bool_arg(x): return bool_str(x)
def get_ip(): return request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr).split(",")[0]


def get_arg(x):
    if request.values.get(x) is None:
        return "0"
    return request.values.get(x)


def int_arg(x):
    try:
        return int(x)
    except ValueError:
        return 0

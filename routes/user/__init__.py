from flask import Blueprint


user = Blueprint('user', __name__)

from .getUsers import *
from .getUserInfo import *
from .updateUserScore import *
from .updateAccSettings import *

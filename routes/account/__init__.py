from flask import Blueprint


account = Blueprint('account', __name__)

from .loginAccount import *
from .registerAccount import *

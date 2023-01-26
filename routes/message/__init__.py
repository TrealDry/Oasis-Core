from flask import Blueprint


message = Blueprint('message', __name__)

from .getMessages import *
from .uploadMessage import *
from .deleteMessage import *
from .downloadMessage import *

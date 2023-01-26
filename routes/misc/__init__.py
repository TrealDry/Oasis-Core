from flask import Blueprint


misc = Blueprint('misc', __name__)

from .likeItem import *
from .getSongInfo import *
from .syncAccount import *
from .backupAccount import *
from .getAccountURI import *
from .requestUserAccess import *

from flask import Blueprint


comment = Blueprint('comment', __name__)

from .getComments import *
from .uploadComment import *
from .deleteComment import *
from .getAccComments import *
from .uploadAccComment import *
from .deleteAccComment import *
from .getCommentHistory import *

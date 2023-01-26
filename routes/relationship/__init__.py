from flask import Blueprint


relationship = Blueprint('relationship', __name__)

from .blockUser import *
from .unblockUser import *
from .getUserList import *
from .removeFriend import *
from .getFriendRequests import *
from .uploadFriendRequest import *
from .acceptFriendRequest import *
from .deleteFriendRequests import *

from flask import Blueprint


level = Blueprint('level', __name__)

from .rateDemon import *
from .rateStars import *
from .getLevels import *
from .updateDesc import *
from .uploadLevel import *
from .deleteLevel import *
from .suggestStars import *
from .downloadLevel import *
from .getDailyLevel import *

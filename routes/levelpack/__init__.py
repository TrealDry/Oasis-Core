from flask import Blueprint


levelpack = Blueprint('levelpack', __name__)

from .getMapPacks import *
from .getGauntlets import *

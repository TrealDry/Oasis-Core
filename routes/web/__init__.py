from flask import Blueprint


web = Blueprint('web', __name__)

from .cron import *
from .songAdd import *
from .songDownload import *
from .activateAccount import *

from flask import Blueprint
app_views = Blueprint('app-views', __name__, url_prefix='/api/v1/')

from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.index import *

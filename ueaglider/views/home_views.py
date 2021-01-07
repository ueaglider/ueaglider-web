import flask
from ueaglider.infrastructure.view_modifiers import response
import ueaglider.services.mission_service as mission_service

blueprint = flask.Blueprint('home', __name__, template_folder='templates')

@blueprint.route('/')
@response(template_file='home/index.html')
def index():
    """
    Home page method,
    :returns: counts of total missions, unique gliders and dives completed
    """

    glider_count = mission_service.get_glider_count()
    mission_count = mission_service.get_mission_count()
    dive_count = mission_service.get_dive_count()
    missions_list = mission_service.list_missions()
    return {'glider_count': glider_count,
            'mission_count': mission_count,
            'dive_count': dive_count,
            'mission_list':missions_list}
import flask
import ueaglider.services.json_conversion as json_conversion
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
    timespan = int(missions_list[0].EndDate.strftime("%Y")) - int(missions_list[-1].EndDate.strftime("%Y"))
    mission_loc = mission_service.mission_loc(filter=True)
    mission_targets = json_conversion.targets_to_json(mission_loc, mission_tgt=True)
    return {'glider_count': glider_count,
            'mission_count': mission_count,
            'dive_count': dive_count,
            'mission_list': missions_list,
            'mission_tgts': mission_targets,
            'timespan': timespan}

import flask
from ueaglider.infrastructure.view_modifiers import response
import ueaglider.services.mission_service as mission_service

blueprint = flask.Blueprint('missions', __name__, template_folder='templates')


@blueprint.route('/mission<int:mission_id>')
@response(template_file='missions/mission.html')
def missions(mission_id: int):
    """
    Home page method,
    :returns: counts of total missions, unique gliders and dives completed
    """
    mission = mission_service.get_mission_by_id(mission_id)

    return {'mission': mission}

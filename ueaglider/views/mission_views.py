import flask
from ueaglider.infrastructure.view_modifiers import response
import ueaglider.services.mission_service as mission_service

blueprint = flask.Blueprint('missions', __name__, template_folder='templates')


@blueprint.route('/mission<int:mission_id>')
@response(template_file='missions/mission.html')
def missions(mission_id: int):
    """
    Mission page method,
    :returns:
    mission: selected mission information
    targets: targets for this this mission
    target_dict: targets formatted to JSON style dict for JS map
    """
    mission = mission_service.get_mission_by_id(mission_id)
    targets = mission_service.get_mission_targets(mission_id)
    target_dict = mission_service.targets_to_json(targets)
    dives, gliders = mission_service.get_mission_dives(mission_id)
    divesdict = mission_service.dives_to_json(dives, gliders)
    return {'mission': mission,
            'targets': targets,
            'targetdict': target_dict,
            'divesdict': divesdict
            }

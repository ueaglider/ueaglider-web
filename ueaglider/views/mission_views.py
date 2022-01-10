import os
import sys
import flask

from ueaglider.services import mission_service
from ueaglider.viewmodels.mission.mission_viewmodel import MissionViewModel

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

from ueaglider.infrastructure.view_modifiers import response

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
    missions_nums = mission_service.mission_ids()
    id_list = [y for x in missions_nums for y in x]
    if mission_id not in id_list:
        return flask.redirect('/')

    vm = MissionViewModel(mission_id)
    vm.check_dives()
    vm.check_tags()
    vm.add_seals()
    return vm.to_dict()

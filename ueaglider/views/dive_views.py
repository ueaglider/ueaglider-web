import flask
from ueaglider.infrastructure.view_modifiers import response

from ueaglider.viewmodels.dive.dive_viewmodel import DiveViewModel, StatusViewModel, ScienceViewModel


blueprint = flask.Blueprint('dives', __name__, template_folder='templates')


@blueprint.route('/mission<int:mission_id>/glider<int:glider_num>/science')
@response(template_file='missions/dive.html')
def science(mission_id: int, glider_num: int):
    """
    Science page method,
    :returns:
    dive_plots: list of paths to images associated with the dive
    """
    vm = ScienceViewModel(mission_id, glider_num)
    return vm.to_dict()



@blueprint.route('/mission<int:mission_id>/glider<int:glider_num>/status')
@response(template_file='missions/dive.html')
def status(mission_id: int, glider_num: int):
    """
    Science page method,
    :returns:
    dive_plots: list of paths to images associated with the dive
    """
    vm = StatusViewModel(mission_id, glider_num)
    return vm.to_dict()


@blueprint.route('/mission<int:mission_id>/glider<int:glider_num>/dive<int:dive_num>')
@response(template_file='missions/dive.html')
def dive(mission_id: int, glider_num: int, dive_num: int):
    """
    Dives page method,
    :returns:
    dive_plots: list of paths to images associated with the dive
    """
    vm = DiveViewModel(mission_id, glider_num, dive_num)
    return vm.to_dict()


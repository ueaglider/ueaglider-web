import flask
from flask import request

from ueaglider.infrastructure.view_modifiers import response

from ueaglider.viewmodels.dive.dive_viewmodel import DiveViewModel, StatusViewModel, ScienceViewModel


blueprint = flask.Blueprint('dives', __name__, template_folder='templates')


@blueprint.route('/mission<int:mission_id>/glider<int:glider_num>/science')
@response(template_file='dive/dive.html')
def science(mission_id: int, glider_num: int):
    """
    Science page method,
    :returns:
    dive_plots: list of paths to images associated with the dive
    """
    vm = ScienceViewModel(mission_id, glider_num, False)
    return vm.to_dict()


@blueprint.route('/mission<int:mission_id>/glider<int:glider_num>/science_python')
@response(template_file='dive/dive.html')
def science_python(mission_id: int, glider_num: int):
    """
    Python Science page method,
    :returns:
    dive_plots: list of paths to images associated with the dive
    """
    vm = ScienceViewModel(mission_id, glider_num, True)
    vm.python_plots = True
    return vm.to_dict()


@blueprint.route('/mission<int:mission_id>/glider<int:glider_num>/status')
@response(template_file='dive/dive.html')
def status(mission_id: int, glider_num: int):
    """
    Science page method,
    :returns:
    dive_plots: list of paths to images associated with the dive
    """
    vm = StatusViewModel(mission_id, glider_num)
    return vm.to_dict()


@blueprint.route('/mission<int:mission_id>/glider<int:glider_num>/dive<int:dive_num>')
@response(template_file='dive/dive.html')
def dive(mission_id: int, glider_num: int, dive_num: int):
    """
    Dives page method,
    :returns:
    dive_plots: list of paths to images associated with the dive
    """
    vm = DiveViewModel(mission_id, glider_num, dive_num)
    if not vm.dive:
        return flask.redirect(f'/mission{str(mission_id)}')
    return vm.to_dict()


@blueprint.route('/DIVES/pilotting.php')
@response(template_file='missions/old_dive.html')
def old_php():
    """
    Dives page method,
    :returns:
    dive_plots: list of paths to images associated with the dive
    """
    glider_num = request.args.get('gliderNo')
    mission_id = request.args.get('missionNo')
    dive_num = request.args.get('diveNo')
    if not dive_num or not mission_id or not glider_num:
        vm = DiveViewModel(1, 1, 1)
        return vm.to_dict()
    vm = DiveViewModel(mission_id, glider_num, dive_num)
    return vm.to_dict()


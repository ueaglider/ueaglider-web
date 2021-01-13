import flask
from ueaglider.infrastructure.view_modifiers import response
import glob
import os
import sys
from pathlib import Path
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)
blueprint = flask.Blueprint('dives', __name__, template_folder='templates')


@blueprint.route('/mission<int:mission_id>/glider<int:glider_num>/science')
@response(template_file='missions/dive.html')
def science(mission_id: int, glider_num: int):
    """
    Science page method,
    :returns:
    dive_plots: list of paths to images associated with the dive
    """
    folder_path = Path(folder)
    path_add = 'static/img/dives/Science' + str(mission_id) + '/' + str(glider_num) + '/Monitor'
    dive_path = folder_path / path_add
    figure_paths = sorted(dive_path.glob('*'))
    figure_strings = []
    dive_plot_paths = []
    for path in figure_paths:
        figure_strings.append(str(path))
        dive_plot_paths.append(str(path)[30:])
    links_dict = {
        'glider status': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/status",
        'science': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/science",
        'mission page': "/mission" + str(mission_id),
    }
    return {
        'dive_plots': dive_plot_paths,
        'links_dict': links_dict
    }

@blueprint.route('/mission<int:mission_id>/glider<int:glider_num>/status')
@response(template_file='missions/dive.html')
def status(mission_id: int, glider_num: int):
    """
    Science page method,
    :returns:
    dive_plots: list of paths to images associated with the dive
    """

    folder_path = Path(folder)
    path_add = 'static/img/dives/Mission' + str(mission_id) + '/' + str(glider_num) + '/Monitor'
    dive_path = folder_path / path_add
    figure_paths = sorted(dive_path.glob('*'))
    figure_strings = []
    dive_plot_paths = []
    for path in figure_paths:
        figure_strings.append(str(path))
        dive_plot_paths.append(str(path)[30:])
    links_dict = {
        'glider status': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/status",
        'science': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/science",
        'mission page': "/mission" + str(mission_id),
    }
    return {
        'dive_plots': dive_plot_paths,
        'links_dict': links_dict
    }

@blueprint.route('/mission<int:mission_id>/glider<int:glider_num>/dive<int:dive_num>')
@response(template_file='missions/dive.html')
def dive(mission_id: int, glider_num: int, dive_num: int):
    """
    Dives page method,
    :returns:
    dive_plots: list of paths to images associated with the dive
    """
    folder_path = Path(folder)
    path_add = 'static/img/dives/Mission' + str(mission_id) + '/' + str(glider_num) + '/Dive' + str(dive_num).zfill(4)
    dive_path = folder_path / path_add
    figure_paths = sorted(dive_path.glob('*'))
    figure_strings = []
    dive_plot_paths = []
    for path in figure_paths:
        figure_strings.append(str(path))
        dive_plot_paths.append(str(path)[30:])
    links_dict = {
        'prev dive': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/dive" + str(dive_num - 1),
        'glider status': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/status",
        'science': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/science",
        'mission page': "/mission" + str(mission_id),
        'next dive': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/dive" + str(dive_num + 1),
    }
    return {
        'path': figure_strings,
        'dive_plots': dive_plot_paths,
        'links_dict': links_dict
    }

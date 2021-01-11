import flask
from ueaglider.infrastructure.view_modifiers import response
import glob
import os

blueprint = flask.Blueprint('dives', __name__, template_folder='templates')


@blueprint.route('/mission<int:mission_id>/glider<int:glider_num>/dive<int:dive_num>')
@response(template_file='missions/dive.html')
def dive(mission_id: int, glider_num: int, dive_num: int):
    """
    Dives page method,
    :returns:
    dive_plots: list of paths to images associated with the dive
    """
    dive_glob = glob.glob(os.path.join('static/img/dives/Mission' + str(mission_id)
                                       + '/' + str(glider_num)
                                       + '/Dive' + str(dive_num).zfill(4), '*.png'))
    dive_plot_paths = []
    for item in dive_glob:
        path = '/' + item
        dive_plot_paths.append(path)
    dive_plot_paths.sort()
    links_dict = {
        'prev dive': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/dive" + str(dive_num-1),
        'glider status': "stat",
        'science': "scient",
        'mission page': "/mission"+str(mission_id),
        'next dive': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/dive" + str(dive_num + 1),
    }
    return {
        'dive_plots': dive_plot_paths,
        'links_dict': links_dict
    }

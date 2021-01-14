import flask
from ueaglider.infrastructure.view_modifiers import response
import ueaglider.services.mission_service as mission_service

blueprint = flask.Blueprint('glider', __name__, template_folder='templates')


@blueprint.route('/gliders')
@response(template_file='missions/gliders_list.html')
def gliders_list():
    """
    :return:
    list of all gliders and links to them
    """
    glider_list = mission_service.list_gliders()
    return {
        'glider_list': glider_list
    }


@blueprint.route('/gliders/SG<int:glider_num>')
@response(template_file='missions/glider.html')
def gliders(glider_num: int):
    """
    :param glider_num: the glider number e.g. SG637
    :return:
    info on the glider and its missions
    """
    glider_data, mission_ids = mission_service.glider_info(glider_num)
    dives_count = mission_service.get_dive_count(filter_glider=glider_data.GliderID)
    missions = mission_service.list_missions(filter_missions=True, mission_ids=mission_ids)
    return {
        'glider_data': glider_data,
        'mission_list': missions,
        'dives_count': dives_count
    }

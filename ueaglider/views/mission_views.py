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
    missions_list = mission_service.list_missions()
    mission = mission_service.get_mission_by_id(mission_id)
    targets = mission_service.get_mission_targets(mission_id)
    waypoints = mission_service.get_mission_waypoints(mission_id)
    waypoint_dict = mission_service.waypoints_to_json(waypoints)
    target_dict = mission_service.targets_to_json(targets)
    dives, mission_gliders, dives_by_glider, most_recent_dives = mission_service.get_mission_dives(mission_id)
    dives_by_glider_json = []
    for dives_list in dives_by_glider:
        dives_json, dive_page_links = mission_service.dives_to_json(dives_list, mission_gliders)
        dives_by_glider_json.append(dives_json)
    divesdict, dive_page_links = mission_service.dives_to_json(dives, mission_gliders)
    recentdivesdict, __ = mission_service.dives_to_json(most_recent_dives, mission_gliders)
    mission_plots = [
        'static/img/dives/Mission' + str(mission_id) + '/map.png'
    ]

    return {'mission': mission,
            'mission_list': missions_list,
            'targets': targets,
            'targetdict': target_dict,
            'divesdict': divesdict,
            'recentdivesdict': recentdivesdict,
            'missionplots': mission_plots,
            'dive_page_links': dive_page_links,
            'waypointdict': waypoint_dict,
            'dives_by_glider_json': dives_by_glider_json,
            }


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
    glider_data = mission_service.glider_info(glider_num)
    print(glider_data.Name)
    return {
        'glider_data': glider_data
    }

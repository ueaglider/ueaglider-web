import flask

import ueaglider.services.json_conversion as json_conversion
from ueaglider.infrastructure.view_modifiers import response
import ueaglider.services.mission_service as mission_service
import json
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
    waypoint_dict = json_conversion.waypoints_to_json(waypoints)
    target_dict = json_conversion.targets_to_json(targets)
    dives, mission_gliders, dives_by_glider, most_recent_dives = mission_service.get_mission_dives(mission_id)
    dives_by_glider_json = []
    for dives_list in dives_by_glider:
        dives_json, dive_page_links = json_conversion.dives_to_json(dives_list, mission_gliders)
        dives_by_glider_json.append(dives_json)
    divesdict, dive_page_links = json_conversion.dives_to_json(dives, mission_gliders)
    recentdivesdict, __ = json_conversion.dives_to_json(most_recent_dives, mission_gliders)
    mission_plots = [
        'static/img/dives/Mission' + str(mission_id) + '/map.png'
    ]
    isobath_dict = {}
    for depth in [10, 100, 1000]:
        with open('static/json/isobath_' + str(depth) + 'm.json', 'r') as myfile:
            json_in = json.load(myfile)
        isobath_dict['depth_' + str(depth) + '_m'] = json.loads(json_in)

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
            'isobath_dict': isobath_dict,
            }



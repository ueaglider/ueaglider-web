import os
import subprocess
import sys
import flask
import json

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

import ueaglider.services.json_conversion as json_conversion
from ueaglider.infrastructure.view_modifiers import response
import ueaglider.services.mission_service as mission_service

blueprint = flask.Blueprint('missions', __name__, template_folder='templates')

with open(folder + '/secrets.txt') as json_file:
    secrets = json.load(json_file)


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
    print(dives_by_glider_json)
    recentdivesdict, __ = json_conversion.dives_to_json(most_recent_dives, mission_gliders)
    mission_plots = [
        'static/img/dives/Mission' + str(mission_id) + '/map.png'
    ]
    isobath_dict = {}
    if os.path.exists(folder + '/static/json/Mission' + str(mission_id)):
        mission_folder = folder + '/static/json/Mission' + str(mission_id)
    else:
        mission_targets = mission_service.mission_loc(mission_no=mission_id)
        tgt = mission_targets[0]
        if not mission_targets:
            mission_folder = folder + '/static/json/Mission23'
        else:
            subprocess.run([secrets["gebco_python"], "-u",
                            secrets["gebco_exec"],
                            str(tgt.Longitude),
                            str(tgt.Latitude),
                            str(mission_id),
                            ])
            # mission_folder = folder + '/static/json/Mission23'
            mission_folder = folder + '/static/json/Mission' + str(mission_id)
    for depth in [50, 200, 1000]:
        with open(mission_folder + '/isobaths_' + str(depth) + 'm.json', 'r') as myfile:
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

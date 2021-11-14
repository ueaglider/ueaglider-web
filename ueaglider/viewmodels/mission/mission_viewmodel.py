import os
import subprocess
import sys
import json

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, folder)

from ueaglider.viewmodels.shared.viewmodelbase import ViewModelBase
import ueaglider.services.json_conversion as json_conversion
import ueaglider.services.mission_service as mission_service

with open(folder + '/secrets.txt') as json_file:
    secrets = json.load(json_file)


class MissionViewModel(ViewModelBase):
    def __init__(self, mission_id):
        super().__init__()
        self.mission_id = mission_id
        self.mission_list = mission_service.list_missions()
        self.mission = mission_service.get_mission_by_id(mission_id)
        self.targets = mission_service.get_mission_targets(mission_id)
        if not self.targets:
            self.lon, self.lat = 1.236, 52.624
        else:
            self.lon = self.targets[0].Longitude
            self.lat = self.targets[0].Latitude
        self.waypoints = mission_service.get_mission_pins(mission_id)
        self.waypointdict = json_conversion.pins_to_json(self.waypoints)
        self.targetdict = json_conversion.targets_to_json(self.targets)
        isobath_dict = {}
        if os.path.exists(folder + '/static/json/Mission' + str(self.mission_id)):
            mission_folder = folder + '/static/json/Mission' + str(self.mission_id)
        else:
            mission_targets = mission_service.mission_loc(mission_no=self.mission_id)
            if not mission_targets:
                mission_folder = folder + '/static/json/Mission23'
            else:
                tgt = mission_targets[0]
                subprocess.run([secrets["gebco_python"], "-u",
                                secrets["gebco_exec"],
                                str(tgt.Longitude),
                                str(tgt.Latitude),
                                str(self.mission_id),
                                ])
                mission_folder = folder + '/static/json/Mission' + str(self.mission_id)
        for depth in [50, 200, 500, 1000]:
            with open(mission_folder + '/isobaths_' + str(depth) + 'm.json', 'r') as myfile:
                json_in = json.load(myfile)
            isobath_dict['depth_' + str(depth) + '_m'] = json.loads(json_in)
        self.isobath_dict = isobath_dict
        self.missionplots = [
            'static/img/dives/Mission' + str(self.mission_id) + '/map.png'
        ]

    def check_dives(self):
        dives, mission_gliders, dives_by_glider, most_recent_dives = mission_service.get_mission_dives(self.mission_id)
        if not dives:
            self.zoom = 'No dives yet for this mission'
            blank_json_dict = {"type": "FeatureCollection", "features": []}
            self.dive_page_links = []
            self.recentdivesdict = blank_json_dict
            self.dives_by_glider_json = blank_json_dict
            self.dives_by_glider_json_dupe = []
            self.lines_by_glider_json = blank_json_dict
        else:
            dives_by_glider_json = []
            lines_by_glider_json = []
            for dives_list in dives_by_glider:
                dives_json, dive_page_links, line_json = json_conversion.dives_to_json(dives_list, mission_gliders)
                dives_by_glider_json.append(dives_json)
                lines_by_glider_json.append(line_json)
            recentdivesdict, __, __ = json_conversion.dives_to_json(most_recent_dives, mission_gliders)
            self.recentdivesdict = recentdivesdict
            self.dive_page_links = dive_page_links
            self.dives_by_glider_json = dives_by_glider_json
            self.dives_by_glider_json_dupe = dives_by_glider_json
            self.lines_by_glider_json = lines_by_glider_json
            self.zoom = 'normal'

    def check_tags(self):
        tag_locs, mission_tags, locs_by_tag, most_recent_locs = mission_service.get_mission_tag_locs(self.mission_id)
        if not tag_locs:
            blank_json_dict = {"type": "FeatureCollection", "features": []}
            self.recentlocsdict = blank_json_dict
            self.locs_by_tag_json = blank_json_dict
            self.locs_by_tag_json_dupe = []
            self.lines_by_tag_json = blank_json_dict
        else:
            locs_by_tag_json = []
            lines_by_tag_json = []
            for dives_list in locs_by_tag:
                dives_json, dive_page_links, line_json = json_conversion.tags_to_json(dives_list, mission_tags)
                locs_by_tag_json.append(dives_json)
                lines_by_tag_json.append(line_json)

            recentdivesdict, __, __ = json_conversion.tags_to_json(most_recent_locs, mission_tags)
            self.recentlocsdict = recentdivesdict
            self.locs_by_tag_json = locs_by_tag_json
            self.locs_by_tag_json_dupe = locs_by_tag_json
            self.lines_by_tag_json = lines_by_tag_json


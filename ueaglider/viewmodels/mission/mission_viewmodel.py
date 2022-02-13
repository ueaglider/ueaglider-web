import os
import subprocess
import sys
import json
import glob
import datetime
import pandas as pd
import numpy as np

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
        self.start = self.request_dict.start
        self.end = self.request_dict.end
        self.start_time = self.request_dict.start_time
        self.end_time = self.request_dict.end_time
        if self.start_time or self.end_time:
            self.hidef_ship_track = True
        else:
            self.hidef_ship_track = False
        if not self.start:
            self.start_dt = datetime.datetime(2000, 1, 1)
        else:
            if not self.start_time:
                start_hour = 0
                start_min = 0
            else:
                start_hour = int(self.start_time[:2])
                start_min = int(self.start_time[3:])
            self.start_dt = datetime.datetime(int(self.start[:4]), int(self.start[5:7]), int(self.start[8:]),
                                              start_hour, start_min)
        if not self.end:
            self.end_dt = datetime.datetime(2100, 1, 1)
        else:
            if not self.end_time:
                end_hour = 23
                end_min = 59
            else:
                end_hour = int(self.end_time[:2])
                end_min = int(self.end_time[3:])
            self.end_dt = datetime.datetime(int(self.end[:4]), int(self.end[5:7]), int(self.end[8:]),
                                            end_hour, end_min)

    def check_dives(self):
        if self.mission_id >= 62:
            dives, mission_gliders, dives_by_glider, most_recent_dives = mission_service.get_mission_dives(self.mission_id,
                                                                        start=self.start_dt, end=self.end_dt)
        else:
            dives, mission_gliders, dives_by_glider, most_recent_dives = mission_service.get_mission_dives(self.mission_id)

        if not dives_by_glider:
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
        qualities_lists = (
            ('G', '3'),
            ('G', '3', '2', '1'),
            ('G', '3', '2', '1', '0', 'A', 'B', 'Z'),
        )
        quality_levels = ('best', 'defined', 'all')
        recentlocsdict, locs_by_tag_json, lines_by_tag_json = [], [], []
        for level in range(3):
            qual = qualities_lists[level]
            tag_locs, mission_tags, locs_by_tag, most_recent_locs = mission_service.get_mission_tag_locs(self.mission_id,
                                                                                                         qualities=qual)
            if not tag_locs:
                blank_json_dict = {"type": "FeatureCollection", "features": []}
                recentlocsdict.append(blank_json_dict)
                locs_by_tag_json.append(blank_json_dict)
                lines_by_tag_json.append(blank_json_dict)
            else:
                locs_by_tag_json_i = []
                lines_by_tag_json_i = []
                for dives_list in locs_by_tag:
                    dives_json, dive_page_links, line_json = json_conversion.tags_to_json(dives_list, mission_tags)
                    locs_by_tag_json_i.append(dives_json)
                    lines_by_tag_json_i.append(line_json)

                recentdivesdict, __, __ = json_conversion.tags_to_json(most_recent_locs, mission_tags)
                recentlocsdict.append(recentdivesdict)
                locs_by_tag_json.append(locs_by_tag_json_i)
                lines_by_tag_json.append(lines_by_tag_json_i)
        self.recentlocsdict = recentlocsdict
        self.locs_by_tag_json = locs_by_tag_json
        self.lines_by_tag_json = lines_by_tag_json

    def add_seals(self):
        locs, seals = mission_service.get_seals()
        self.seals_dict , self.seals_lines_dict = json_conversion.seals_to_json(locs, seals)

    def add_events(self):
        blank_json_dict = {"type": "FeatureCollection", "features": []}
        event_dir = folder+'/static/nbp_data/'
        for dataset in ['ctd', 'tmc', 'core', 'thor', 'hugin', 'alr', 'vmp', 'ship', 'wp', 'points', 'ship_days',
                        'hugin_bottle', 'fish']:
            try:
                if self.hidef_ship_track and dataset == 'ship':
                    df = pd.read_csv(f"{event_dir}1_min_nrt.csv", parse_dates=['datetime'])
                    df_a = df[df.datetime > self.start_dt]
                    df_cut = df_a[df_a.datetime < self.end_dt]
                    today = df.julian_day.values[-1]
                    jul_days = np.unique(df_cut.julian_day)
                    items = []
                    for day in jul_days:
                        if day == today:
                            last_day = True
                        else:
                            last_day = False
                        df_sub = df_cut[df_cut.julian_day == day]
                        items.append(mission_service.track_to_json(df_sub, today=last_day))
                    tgtdict = {
                        "type": "FeatureCollection",
                        "features": items
                    }
                    self.__setattr__(f"{dataset}_dict", tgtdict)
                    continue
                with open(f"{event_dir}{dataset}.json") as json_to_load:
                    json_dict = json.load(json_to_load)
                features = json_dict['features']
                features_in_time = []
                for feature in features:
                    try:
                        start = datetime.datetime.fromisoformat(feature['start'])
                    except:
                        try:
                            start = datetime.datetime.fromisoformat(feature['end'])
                        except:
                            features_in_time.append(feature)
                            continue
                    try:
                        end = datetime.datetime.fromisoformat(feature['end'])
                    except:
                        end = start
                    if self.start_dt <= start <= self.end_dt or self.start_dt <= end <= self.end_dt:
                        features_in_time.append(feature)
                    json_dict['features'] = features_in_time
                self.__setattr__(f"{dataset}_dict", json_dict)
            except:
                self.__setattr__(f"{dataset}_dict", blank_json_dict)
        try:
            amsr_dirs = glob.glob(f'{folder}/static/img/tiles/AMSR*')
            amsr_dirs.sort()
            amsr_dict = {}
            for amsr in amsr_dirs:
                amsr_date = amsr.split('/')[-1][-10:]
                date_str = amsr_date.replace('_', '-')
                amsr_dict[date_str] = amsr[-32:]
            self.amsr_dict = amsr_dict
        except:
            self.amsr_dict = {}

        try:
            modis_dirs = glob.glob(f'{folder}/static/img/tiles/MODIS*')
            modis_dirs.sort()
            modis_dict = {}
            for modis in modis_dirs:
                modis_date = modis.split('/')[-1][-8:]
                date_str = f"{modis_date[:4]}-{modis_date[4:6]}-{modis_date[6:]}"
                modis_dict[date_str] = modis[-32:]
            self.modis_dict = modis_dict
        except:
            self.modis_dict = {}

        try:
            polar_dirs = glob.glob(f'{folder}/static/img/tiles/polarview/*')
            polar_dirs.sort()
            polar_dict = {}
            for amsr in polar_dirs:
                amsr_date = amsr.split('/')[-1]
                date_str = f"{amsr_date[:4]}-{amsr_date[4:6]}-{amsr_date[6:8]} {amsr_date[9:11]}:{amsr_date[11:13]}:{amsr_date[13:15]}"
                polar_dict[date_str] = amsr[-42:]
            self.polar_dict = polar_dict
        except:
            self.polar_dict = {}
        self.pre_start_time = self.start_time
        self.pre_end_time = self.end_time
        self.start_time = None
        self.end_time = None

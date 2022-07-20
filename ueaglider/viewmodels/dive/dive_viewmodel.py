from ueaglider.services import mission_service, json_conversion
from ueaglider.viewmodels.shared.viewmodelbase import ViewModelBase
import flask
import os
import sys
from pathlib import Path

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, folder)


class ScienceViewModel(ViewModelBase):
    def __init__(self, mission_id, glider_num, python_plot):
        super().__init__()
        self.mission_num = mission_id
        self.glider_num = glider_num
        self.python_plots = python_plot
        folder_path = Path(folder)
        # Find the absolute path to the figures
        if self.python_plots:
            path_add = 'static/img/dives/Mission' + str(mission_id) + '/' + str(glider_num) + '/Science_python'
        else:
            path_add = 'static/img/dives/Mission' + str(mission_id) + '/' + str(glider_num) + '/Science'
        dive_path = folder_path / path_add
        figure_paths = sorted(dive_path.glob('*'))
        dive_plot_paths = []
        for path in figure_paths:
            path_str = str(path)
            # Cut the path to each figure so it starts from 'static' directory in app's home directory
            rel_path = path_str[path_str.find('/static'):]
            dive_plot_paths.append(rel_path)
        self.links_dict = {
            'glider status': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/status",
            'science': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/science",
            'science_python': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/science_python",
            'mission page': "/mission" + str(mission_id),
        }
        if not dive_plot_paths:
            dive_plot_paths = ['/static/img/dives/hedge.png']
        self.dive_plots = dive_plot_paths


class StatusViewModel(ViewModelBase):
    def __init__(self, mission_id, glider_num):
        super().__init__()
        self.mission_num = mission_id
        self.glider_num = glider_num
        folder_path = Path(folder)
        # Find the absolute path to the figures
        path_add = 'static/img/dives/Mission' + str(mission_id) + '/' + str(glider_num) + '/Monitor'
        dive_path = folder_path / path_add
        figure_paths = sorted(dive_path.glob('*'))
        dive_plot_paths = []
        for path in figure_paths:
            path_str = str(path)
            # Cut the path to each figure so it starts from 'static' directory in app's home directory
            rel_path = path_str[path_str.find('/static'):]
            dive_plot_paths.append(rel_path)
        self.links_dict = {
            'glider status': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/status",
            'science': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/science",
            'science_python': "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/science_python",
            'mission page': "/mission" + str(mission_id),
        }
        if not dive_plot_paths:
            dive_plot_paths = ['/static/img/dives/hedge.png']
        self.dive_plots = dive_plot_paths


class DiveViewModel(ViewModelBase):
    def __init__(self, mission_id, glider_num, dive_num):
        super().__init__()
        folder_path = Path(folder)
        # Find the absolute path to the figures
        path_add = 'static/img/dives/Mission' + str(mission_id) + '/' + str(glider_num) + '/Dive' + str(dive_num).zfill(
            4)
        dive_path = folder_path / path_add
        figure_paths = sorted(dive_path.glob('*'))
        dive_plot_paths = []
        self.mission_num = mission_id
        self.mission_list = mission_service.list_missions()
        self.glider_num = glider_num
        self.dive_num = dive_num
        self.dive = mission_service.get_dive(glider_num, dive_num, mission_id)
        dives, mission_gliders, dives_by_glider, most_recent_dives = mission_service.get_mission_dives(self.mission_num)
        dives_by_glider_json = []
        for dives_list in dives_by_glider:
            dives_json, dive_page_links, line_json = json_conversion.dives_to_json(dives_list, mission_gliders)
            dives_by_glider_json.append(dives_json)
        self.dives_by_glider_json = dives_by_glider_json
        self.dives = mission_service.get_dive_nums(self.glider_num, self.mission_num)

        if not self.dive:
            return
        if self.dive.Status:
            status = self.dive.Status.split(':')
            names = ['dive num', 'call cycle', 'calls made', 'no-comm count', 'internal mission number',
                     'reboot count', 'error code', 'AD pitch', 'AD roll', 'AD VBD', 'Pitch', 'Depth',
                     '10 V voltage', '24 V voltage', 'internal pressure', 'internal RH']
            print_fields = ['call cycle', 'calls made', 'no-comm count', 'error code',
                            '10 V voltage', '24 V voltage', 'internal pressure', 'internal RH']
            status_str = ''
            for name, stat in zip(names, status):
                if name in print_fields:
                    status_str = status_str + name + ': ' + '<b>' + str(stat) + '</b>' + ' | '
            self.status_str = status_str
        for path in figure_paths:
            path_str = str(path)
            # Cut the path to each figure so it starts from 'static' directory in app's home directory
            rel_path = path_str[path_str.find('/static'):]
            dive_plot_paths.append(rel_path)
        self.links_dict = {}
        prev_dive, next_dive = mission_service.adjacent_dives(self.glider_num, self.dive_num, self.mission_num)
        if prev_dive:
            self.links_dict['prev dive'] = f"/mission{str(mission_id)}/glider{str(glider_num)}/dive{str(prev_dive[0])}"

        self.links_dict['glider status'] = "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/status"
        self.links_dict['science'] = "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/science"
        self.links_dict['science_python'] = "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/science_python"
        self.links_dict['mission page'] = "/mission" + str(mission_id)
        if next_dive:
            self.links_dict['next dive'] = f"/mission{str(mission_id)}/glider{str(glider_num)}/dive{str(next_dive[0])}"

        if not dive_plot_paths:
            dive_plot_paths = ['/static/img/dives/hedge.png']
        self.dive_plots = dive_plot_paths

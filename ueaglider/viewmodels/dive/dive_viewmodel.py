from ueaglider.services.mission_service import get_dive
from ueaglider.viewmodels.shared.viewmodelbase import ViewModelBase
import flask
import os
import sys
from pathlib import Path

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, folder)

class ScienceViewModel(ViewModelBase):
    def __init__(self, mission_id, glider_num):
        super().__init__()
        self.mission_num = mission_id
        self.glider_num = glider_num
        folder_path = Path(folder)
        # Find the absolute path to the figures
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
        self.glider_num = glider_num
        self.dive_num = dive_num
        self.dive = get_dive(glider_num, dive_num, mission_id)
        if not self.dive:
            return
        if self.dive.Status:
            status = self.dive.Status.split(':')
            names = ['dive num', 'call cycle', 'calls made', 'no-comm count', 'internal mission number',
                             'reboot count', 'error code', 'AD pitch', 'AD roll', 'AD VBD', 'Pitch', 'Depth',
                             '10 V voltage', '24 V voltage', 'internal pressure', 'internal RH']
            status_str = ''
            for name, stat in zip(names, status):
                 status_str = status_str + name + ': ' + str(stat) + '<br>'
            self.status_str = status_str
        for path in figure_paths:
            path_str = str(path)
            # Cut the path to each figure so it starts from 'static' directory in app's home directory
            rel_path = path_str[path_str.find('/static'):]
            dive_plot_paths.append(rel_path)
        self.links_dict = {}
        if get_dive(glider_num, dive_num-1, mission_id):
            self.links_dict['prev dive'] = "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/dive" + str(int(dive_num) - 1)

        self.links_dict['glider status'] = "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/status"
        self.links_dict['science'] = "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/science"
        self.links_dict['mission page'] = "/mission" + str(mission_id)
        if get_dive(glider_num, dive_num+1, mission_id):
            self.links_dict['next dive'] = "/mission" + str(mission_id) + "/glider" + str(glider_num) + "/dive" + str(int(dive_num) + 1)

        if not dive_plot_paths:
            dive_plot_paths = ['/static/img/dives/hedge.png']
        self.dive_plots = dive_plot_paths

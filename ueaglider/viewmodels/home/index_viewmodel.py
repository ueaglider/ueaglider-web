import ueaglider.services.glider_service
from ueaglider.services import mission_service, json_conversion
from ueaglider.viewmodels.shared.viewmodelbase import ViewModelBase

class IndexViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.glider_count = ueaglider.services.glider_service.get_glider_count()
        self.mission_count = mission_service.get_mission_count()
        self.dive_count = mission_service.get_dive_count()
        self.mission_list = mission_service.list_missions()
        self.timespan = int(self.mission_list[0].EndDate.strftime("%Y")) - int(self.mission_list[-1].EndDate.strftime("%Y"))
        self.mission_loc = mission_service.mission_loc(filter_missions=True)
        self.mission_tgts = json_conversion.targets_to_json(self.mission_loc, mission_tgt=True)

    def check_dives(self):
        dives = mission_service.get_recent_dives(hours=16000)
        if not dives:
            self.recentdives = []
        else:
            self.recentdives = dives[-5:]

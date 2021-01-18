from ueaglider.services import mission_service, json_conversion
from ueaglider.viewmodels.shared.viewmodelbase import ViewModelBase

class GliderListViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.glider_list = mission_service.list_gliders()



class GliderViewModel(ViewModelBase):
    def __init__(self, glider_num):
        super().__init__()
        self.glider_list = mission_service.list_gliders()

        self.glider_data, mission_ids = mission_service.glider_info(glider_num)
        self.dives_count = mission_service.get_dive_count(filter_glider=self.glider_data.GliderID)
        self.mission_list = mission_service.list_missions(filter_missions=True, mission_ids=mission_ids)
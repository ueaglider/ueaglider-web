import ueaglider.services.glider_service
from ueaglider.services import mission_service
from ueaglider.viewmodels.shared.viewmodelbase import ViewModelBase

class GliderListViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.glider_list = ueaglider.services.glider_service.list_gliders()
        self.other_glider_list = ueaglider.services.glider_service.list_gliders(non_uea=True)



class GliderViewModel(ViewModelBase):
    def __init__(self, glider_num):
        super().__init__()
        self.glider_list = ueaglider.services.glider_service.list_gliders()

        self.glider_data, mission_ids = ueaglider.services.glider_service.glider_info(glider_num)
        self.dives_count = mission_service.get_dive_count(filter_glider=self.glider_data.GliderID)
        self.mission_list = mission_service.list_missions(filter_missions=True, mission_id_list=mission_ids)
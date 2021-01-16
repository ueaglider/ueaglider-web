from ueaglider.services import user_service
from ueaglider.viewmodels.shared.viewmodelbase import ViewModelBase

class IndexViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.user = user_service.find_user_by_id(self.user_id)

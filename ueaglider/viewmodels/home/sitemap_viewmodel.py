import flask

from ueaglider.services import glider_service
from ueaglider.viewmodels.shared.viewmodelbase import ViewModelBase


class SiteMapViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.gliders = glider_service.list_gliders()
        self.last_updated_text = "2019-07-15" #TODO autoupdate this
        self.site = "{}://{}".format(flask.request.scheme, flask.request.host)

from ueaglider.services import mission_service
from ueaglider.viewmodels.shared.viewmodelbase import ViewModelBase


class AddPinViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.missionid = self.request_dict.missionid
        self.name = self.request_dict.name.strip()
        self.lon = self.request_dict.lon
        self.lat = self.request_dict.lat
        self.info = self.request_dict.info.strip()

    def validate(self):
        if not self.missionid or not self.name.strip() or not self.lon or not self.lat or not self.info:
            self.error = 'Please fill in all fields'
        missions = mission_service.mission_ids()
        id_list = [y for x in missions for y in x]
        self.missionid = int(self.missionid)
        if self.missionid not in id_list:
            self.error = 'Mission ' + str(self.missionid) + ' does not exist'
        self.lat = float(self.lat)
        self.lon = float(self.lon)


class AddTargetViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.missionid = self.request_dict.missionid
        self.name = self.request_dict.name.strip()
        self.lon = self.request_dict.lon
        self.lat = self.request_dict.lat
        self.radius = self.request_dict.radius
        self.goto = self.request_dict.goto

    def validate(self):
        if not self.missionid or not self.name.strip() or not self.lon or not self.lat or not self.radius or not self.goto:
            self.error = 'Please fill in all fields'
        missions = mission_service.mission_ids()
        id_list = [y for x in missions for y in x]
        self.missionid = int(self.missionid)
        if self.missionid not in id_list:
            self.error = 'Mission ' + str(self.missionid) + ' does not exist'
        self.lat = float(self.lat)
        self.lon = float(self.lon)
        self.radius = int(self.radius)


class AddMissionViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        missions_nums = mission_service.mission_ids()
        id_list = [y for x in missions_nums for y in x]
        self.missions = id_list
        self.missionid = self.request_dict.missionid
        if self.missionid:
            self.missionid = int(self.missionid)
        self.name = self.request_dict.name.strip()
        self.start = self.request_dict.start
        self.end = self.request_dict.end
        self.info = self.request_dict.info.strip()

    def validate(self):
        if not self.missionid or not self.name.strip() or not self.end or not self.start or not self.info.strip():
            self.error = 'Please fill in all fields'
        if self.missionid in self.missions:
            self.error = 'Mission ' + str(self.missionid) + ' already exists'


class RemovePinViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.pins, pin_ids = mission_service.get_pins()
        self.all_pin_ids = [y for x in pin_ids for y in x]

        self.pin_id = self.request_dict.pin_id
        self.pin_id_confirm = self.request_dict.pin_id_confirm

    def validate(self):
        if not self.pin_id or not self.pin_id_confirm:
            self.error = 'Please fill in all fields'
        self.pin_id = int(self.pin_id)
        self.pin_id_confirm = int(self.pin_id_confirm)
        if self.pin_id != self.pin_id_confirm:
            self.error = 'Supplied values do not match'
        if self.pin_id not in self.all_pin_ids:
            self.error = 'Pin ID not found in table'

    def update(self):
        self.pins, __ = mission_service.get_pins()
        self.pin_id = ''
        self.pin_id_confirm = ''


class RemoveTargetViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.targets, target_ids = mission_service.get_targets()
        self.all_target_ids = [y for x in target_ids for y in x]

        self.target_id = self.request_dict.target_id
        self.target_id_confirm = self.request_dict.target_id_confirm

    def validate(self):
        if not self.target_id or not self.target_id_confirm:
            self.error = 'Please fill in all fields'
        self.target_id = int(self.target_id)
        self.target_id_confirm = int(self.target_id_confirm)
        if self.target_id != self.target_id_confirm:
            self.error = 'Supplied values do not match'
        if self.target_id not in self.all_target_ids:
            self.error = 'Target ID not found in table'

    def update(self):
        self.targets, __ = mission_service.get_targets()
        self.target_id = ''
        self.target_id_confirm = ''

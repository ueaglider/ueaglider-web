from ueaglider.data.db_classes import coord_db_decimal
from ueaglider.services import mission_service, glider_service, argos_service
from ueaglider.viewmodels.shared.viewmodelbase import ViewModelBase


class AddPinViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.missionid = self.request_dict.missionid
        self.name = self.request_dict.name.strip()
        self.lon = self.request_dict.lon
        self.lat = self.request_dict.lat
        self.info = self.request_dict.info.strip()
        self.format = str(self.request_dict.format.strip())

    def validate(self):
        if not self.missionid or not self.name.strip() or not self.lon or not self.lat or not self.info:
            self.error = 'Please fill in all fields'
        missions = mission_service.mission_ids()
        id_list = [y for x in missions for y in x]
        self.missionid = int(self.missionid)
        if self.missionid not in id_list:
            self.error = 'Mission ' + str(self.missionid) + ' does not exist'
        if self.format == 'dec_degree':
            self.lat = float(self.lat)
            self.lon = float(self.lon)
        elif self.format == 'deg_min':
            self.lat = coord_db_decimal(float(self.lat))
            self.lon = coord_db_decimal(float(self.lon))
        elif self.format == 'seaglider':
            self.lat = coord_db_decimal(float(self.lat), kongsberg=True)
            self.lon = coord_db_decimal(float(self.lon), kongsberg=True)
        else:
            self.error = 'coordinate format not recognised'
        if abs(self.lat) > 90 or abs(self.lon) > 180:
            self.error = 'coordinates out of bounds'


class AddTargetViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.missionid = self.request_dict.missionid
        self.name = self.request_dict.name.strip()
        self.lon = self.request_dict.lon
        self.lat = self.request_dict.lat
        self.radius = self.request_dict.radius
        self.goto = self.request_dict.goto
        self.format = str(self.request_dict.format.strip())

    def validate(self):
        if not self.missionid or not self.name.strip() or not self.lon or not self.lat or not self.radius or not self.goto:
            self.error = 'Please fill in all fields'
        missions = mission_service.mission_ids()
        id_list = [y for x in missions for y in x]
        self.missionid = int(self.missionid)
        if self.missionid not in id_list:
            self.error = 'Mission ' + str(self.missionid) + ' does not exist'
        if self.format == 'dec_degree':
            self.lat = float(self.lat)
            self.lon = float(self.lon)
        elif self.format == 'deg_min':
            self.lat = coord_db_decimal(float(self.lat))
            self.lon = coord_db_decimal(float(self.lon))
        elif self.format == 'seaglider':
            self.lat = coord_db_decimal(float(self.lat), kongsberg=True)
            self.lon = coord_db_decimal(float(self.lon), kongsberg=True)
        else:
            self.error = 'coordinate format not recognised'
        if abs(self.lat) > 90 or abs(self.lon) > 180:
            self.error = 'coordinates out of bounds'
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


class AddGliderViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        glider_nums = glider_service.glider_nums()
        id_list = [y for x in glider_nums for y in x]
        self.glider_nums = id_list
        self.missionid = self.request_dict.missionid
        if self.missionid:
            self.missionid = int(self.missionid)
        self.name = self.request_dict.name.strip()
        self.glider_num = self.request_dict.glider_num
        if self.glider_num:
            self.glider_num = int(self.glider_num)
        self.info = self.request_dict.info.strip()
        self.ueaglider = self.request_dict.ueaglider
        self.overwrite_check = self.request_dict.overwrite_check

    def validate(self):
        if not self.name.strip() or not self.glider_num or not self.info.strip():
            self.error = 'Please fill in all fields'

        if self.glider_num in self.glider_nums:
            # Error if the glider already exists
            if 'overwrite_check' in self.request_dict:
                # Unless user opted to overwrite it
                self.overwrite_check = True
            else:
                self.error = 'Glider SG' + str(self.glider_num) + ' already exists'
        if 'ueaglider_check' in self.request_dict:
            self.ueaglider = True
        else:
            self.ueaglider = False


class AddTagViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        tag_nums = argos_service.tag_nums()
        id_list = [y for x in tag_nums for y in x]
        self.tag_nums = id_list
        self.missionid = self.request_dict.missionid
        if self.missionid:
            self.missionid = int(self.missionid)
        self.gliderid = self.request_dict.gliderid
        if self.gliderid:
            self.gliderid = int(self.gliderid)
        self.tag_num = self.request_dict.tag_num
        if self.tag_num:
            self.tag_num = int(self.tag_num)
        self.overwrite_check = self.request_dict.overwrite_check

    def validate(self):
        if not self.tag_num or not self.missionid or not self.gliderid:
            self.error = 'Please fill in all fields'

        if self.tag_num in self.tag_nums:
            # Error if the glider already exists
            if 'overwrite_check' in self.request_dict:
                # Unless user opted to overwrite it
                self.overwrite_check = True
            else:
                self.error = 'Tag number' + str(self.tag_num) + ' already exists'



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


class RemoveMissionViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.missions, mission_ids = mission_service.get_missions()
        self.all_mission_ids = [y for x in mission_ids for y in x]

        self.mission_id = self.request_dict.mission_id
        self.mission_id_confirm = self.request_dict.mission_id_confirm

    def validate(self):
        if not self.mission_id or not self.mission_id_confirm:
            self.error = 'Please fill in all fields'
        self.mission_id = int(self.mission_id)
        self.mission_id_confirm = int(self.mission_id_confirm)
        if self.mission_id != self.mission_id_confirm:
            self.error = 'Supplied values do not match'
        elif self.mission_id not in self.all_mission_ids:
            self.error = 'Mission Number not found in table'

    def update(self):
        self.missions, __ = mission_service.get_missions()
        self.mission_id = ''
        self.mission_id_confirm = ''


class RemoveDiveViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.dives, dive_ids = mission_service.get_dives()
        self.all_dive_ids = [y for x in dive_ids for y in x]

        self.dive_id = self.request_dict.dive_id
        self.dive_id_confirm = self.request_dict.dive_id_confirm

    def validate(self):
        if not self.dive_id or not self.dive_id_confirm:
            self.error = 'Please fill in all fields'
        self.dive_id = int(self.dive_id)
        self.dive_id_confirm = int(self.dive_id_confirm)
        if self.dive_id != self.dive_id_confirm:
            self.error = 'Supplied values do not match'
        elif self.dive_id not in self.all_dive_ids:
            self.error = 'Dive ID not found in table'

    def update(self):
        self.dives, __ = mission_service.get_dives()
        self.dive_id = ''
        self.dive_id_confirm = ''


class AssignGliderViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        glider_nums = glider_service.glider_nums()
        id_list = [y for x in glider_nums for y in x]
        self.missions, mission_ids = mission_service.get_missions()
        self.all_mission_ids = [y for x in mission_ids for y in x]
        self.glider_nums = id_list
        self.missionid = self.request_dict.missionid
        if self.missionid:
            self.missionid = int(self.missionid)
        self.glider_num = self.request_dict.glider_num
        if self.glider_num:
            self.glider_num = int(self.glider_num)

    def validate(self):
        if not self.missionid or not self.glider_num:
            self.error = 'Please fill in all fields'

        if self.glider_num not in self.glider_nums:
            # Error if the glider already exists
            self.error = 'Glider SG' + str(self.glider_num) + ' does not exist'

        if self.missionid not in self.all_mission_ids:
            self.error = 'Mission ' + str(self.missionid) + ' does not exist'


class AssignTagViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        tag_nums = argos_service.tag_nums()
        id_list = [y for x in tag_nums for y in x]
        self.missions, mission_ids = mission_service.get_missions()
        self.all_mission_ids = [y for x in mission_ids for y in x]
        self.tag_nums = id_list
        glider_nums = glider_service.glider_nums()
        glider_list = [y for x in glider_nums for y in x]
        self.glider_nums = glider_list
        self.missionid = self.request_dict.missionid
        if self.missionid:
            self.missionid = int(self.missionid)
        self.gliderid = self.request_dict.gliderid
        if self.gliderid:
            self.gliderid = int(self.gliderid)
        self.tag_num = self.request_dict.tag_num
        if self.tag_num:
            self.tag_num = int(self.tag_num)

    def validate(self):
        if self.tag_num not in self.tag_nums:
            self.error = 'Tag number not found in database'

        if not self.tag_num or not self.missionid or not self.gliderid:
            self.error = 'Please fill in all fields'

        if self.gliderid not in self.glider_nums:
            # Error if the glider already exists
            self.error = 'Glider SG' + str(self.gliderid) + ' does not exist'

        if self.missionid not in self.all_mission_ids:
            self.error = 'Mission ' + str(self.missionid) + ' does not exist'

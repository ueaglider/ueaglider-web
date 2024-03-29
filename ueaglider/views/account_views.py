import flask
import os
import sys
import json
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, folder)
with open(folder + '/ueaglider/secrets.txt') as json_file:
    secrets = json.load(json_file)
from ueaglider.infrastructure.view_modifiers import response
from ueaglider.services import user_service, db_edits
from ueaglider.infrastructure import cookie_auth as cookie_auth
from ueaglider.services.db_edits import audit_entry, delete_pin, delete_target, delete_mission, delete_glider, \
    delete_dive, assign_glider, delete_tag, delete_multiple_dives
from ueaglider.viewmodels.account.edit_viewmodel import AddPinViewModel, AddMissionViewModel, AddTargetViewModel, \
    RemovePinViewModel, RemoveTargetViewModel, RemoveMissionViewModel, AddGliderViewModel, RemoveDiveViewModel, \
    AssignGliderViewModel, AddTagViewModel, AssignTagViewModel, RemoveMultipleDivesViewModel
from ueaglider.viewmodels.account.index_viewmodel import AccountIndexViewModel
from ueaglider.viewmodels.account.login_viewmodel import LoginViewModel
from ueaglider.viewmodels.account.register_viewmodel import RegisterViewModel

blueprint = flask.Blueprint('account', __name__, template_folder='templates')


########################## INDEX ##########################

@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    vm = AccountIndexViewModel()

    if not vm.user:
        return flask.redirect('/account/login')
    return vm.to_dict()


########################## REGISTER ##########################


@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    if secrets['accept_new_members'] != "True":
        return flask.redirect('/account/login')
    vm = RegisterViewModel()
    return vm.to_dict()


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    vm = RegisterViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    user = user_service.create_user(vm.name, vm.email, vm.password)

    if not user:
        vm.error = 'The account could not be created'
        return vm.to_dict()

    resp = flask.redirect('/account')
    cookie_auth.set_auth(resp, user.UserID)
    return resp


######################### LOGIN ##########################


@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    vm = LoginViewModel()
    return vm.to_dict()


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    vm = LoginViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    user = user_service.login_user(vm.email, vm.password)
    if not user:
        vm.error = "The account does not exist or the password is wrong."
        return vm.to_dict()

    resp = flask.redirect('/account')
    cookie_auth.set_auth(resp, user.UserID)

    return resp


@blueprint.route('/account/logout')
def logout():
    resp = flask.redirect('/')
    cookie_auth.logout(resp)
    return resp


########################## EDITS ##########################


########################## ADD Pin ##########################


@blueprint.route('/account/add_pin', methods=['GET'])
@response(template_file='account/add_pin.html')
def addpin_get():
    vm = AddPinViewModel()

    if not vm.user_id:
        return flask.redirect('/account/login')
    return vm.to_dict()


@blueprint.route('/account/add_pin', methods=['POST'])
@response(template_file='account/add_pin.html')
def addpin_post():
    vm = AddPinViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    waypoint = db_edits.create_waypoint(vm.missionid, vm.name, vm.lat, vm.lon, vm.info)

    if not waypoint:
        vm.error = 'The waypoint could not be created'
        return vm.to_dict()

    audit_message = 'Add Pin ' + vm.name + ' to mission ' + str(vm.missionid)
    vm.message = 'Success! You have added pin <b>' + vm.name + '</b> to ' + \
                 '<a href="/mission' + str(vm.missionid) + '">' + "Mission " + str(vm.missionid) + "</a>"
    vm.name = ''
    vm.missionid = ''
    vm.lat = ''
    vm.lon = ''
    vm.info = ''
    audit_log = audit_entry(vm.user_id, audit_message)
    if audit_log:
        vm.message = vm.message + '. This entry has been logged'
    return vm.to_dict()


########################## ADD TARGET ##########################


@blueprint.route('/account/add_target', methods=['GET'])
@response(template_file='account/add_target.html')
def addtarget_get():
    vm = AddTargetViewModel()

    if not vm.user_id:
        return flask.redirect('/account/login')
    return vm.to_dict()


@blueprint.route('/account/add_target', methods=['POST'])
@response(template_file='account/add_target.html')
def addtarget_post():
    vm = AddTargetViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    target = db_edits.create_target(vm.missionid, vm.name, vm.lat, vm.lon, vm.radius, vm.goto)

    if not target:
        vm.error = 'The target could not be created'
        return vm.to_dict()

    audit_message = 'Add Target ' + vm.name + ' to mission ' + str(vm.missionid)
    vm.message = 'Success! You have added target <b>' + vm.name + '</b> to ' + \
                 '<a href="/mission' + str(vm.missionid) + '">' + "Mission " + str(vm.missionid) + "</a>"
    vm.name = ''
    vm.missionid = ''
    vm.lat = ''
    vm.lon = ''
    vm.radius = ''
    vm.goto = ''
    audit_log = audit_entry(vm.user_id, audit_message)
    if audit_log:
        vm.message = vm.message + '. This entry has been logged'
    return vm.to_dict()


########################## ADD MISSION ##########################


@blueprint.route('/account/add_mission', methods=['GET'])
@response(template_file='account/add_mission.html')
def addmission_get():
    vm = AddMissionViewModel()

    if not vm.user_id:
        return flask.redirect('/account/login')
    return vm.to_dict()


@blueprint.route('/account/add_mission', methods=['POST'])
@response(template_file='account/add_mission.html')
def addmission_post():
    vm = AddMissionViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()
    mission = db_edits.create_mission(vm.missionid, vm.name, vm.start, vm.end, vm.info)

    if not mission:
        vm.error = 'The mission could not be created'
        return vm.to_dict()

    audit_message = 'Add Mission ' + str(vm.missionid) + ' ' + vm.name
    vm.message = 'Success! You have added ' '<a href="/mission' + str(vm.missionid) + '">' + "Mission " + str(
        vm.missionid) + "</a>" + ': ' + vm.name
    vm.name = ''
    vm.missionid = ''
    vm.start = ''
    vm.end = ''
    vm.info = ''
    audit_log = audit_entry(vm.user_id, audit_message)
    if audit_log:
        vm.message = vm.message + '. This entry has been logged'
    vm.message = vm.message + '<br> would you like to <a href="/account/add_target">add a target?</a>'
    return vm.to_dict()


########################## ADD GLIDER ##########################


@blueprint.route('/account/add_glider', methods=['GET'])
@response(template_file='account/add_glider.html')
def addglider_get():
    vm = AddGliderViewModel()

    if not vm.user_id:
        return flask.redirect('/account/login')
    return vm.to_dict()


@blueprint.route('/account/add_glider', methods=['POST'])
@response(template_file='account/add_glider.html')
def addglider_post():
    vm = AddGliderViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()
    if vm.overwrite_check:
        delete_glider(vm.glider_num)
    glider = db_edits.create_glider(vm.glider_num, vm.name, vm.info, vm.missionid, vm.ueaglider)
    if not glider:
        vm.error = 'The glider could not be created'
        return vm.to_dict()

    audit_message = 'Add glider SG' + str(vm.glider_num) + ' ' + vm.name
    vm.message = 'Success! You have added glider ' '<a href="/gliders/SG' + str(vm.glider_num) + '">' + "SG" + str(
        vm.glider_num) + "</a>" + ': ' + vm.name
    vm.glider_num = ''
    vm.name = ''
    vm.missionid = ''
    vm.info = ''
    audit_log = audit_entry(vm.user_id, audit_message)
    if audit_log:
        vm.message = vm.message + '. This entry has been logged'
    return vm.to_dict()


########################## ADD TAG ##########################


@blueprint.route('/account/add_tag', methods=['GET'])
@response(template_file='account/add_tag.html')
def addtag_get():
    vm = AddTagViewModel()

    if not vm.user_id:
        return flask.redirect('/account/login')
    return vm.to_dict()


@blueprint.route('/account/add_tag', methods=['POST'])
@response(template_file='account/add_tag.html')
def addtag_post():
    vm = AddTagViewModel()
    vm.validate()
    if vm.error:
        return vm.to_dict()
    if vm.overwrite_check:
        delete_tag(vm.tag_num)
    tag = db_edits.create_tag(vm.tag_num, vm.missionid, vm.gliderid)
    if not tag:
        vm.error = 'The tag could not be created'
        return vm.to_dict()

    audit_message = 'Add tag' + str(vm.tag_num)
    vm.message = f'Success! You have added tag {vm.tag_num}'
    vm.tag_num = ''
    vm.missionid = ''
    vm.gliderid = ''
    audit_log = audit_entry(vm.user_id, audit_message)
    if audit_log:
        vm.message = vm.message + '. This entry has been logged'
    return vm.to_dict()

########################## REMOVE PIN ##########################


@blueprint.route('/account/remove_pin', methods=['GET'])
@response(template_file='account/remove_pin.html')
def remove_pin_get():
    vm = RemovePinViewModel()

    if not vm.user_id:
        return flask.redirect('/account/login')
    return vm.to_dict()


@blueprint.route('/account/remove_pin', methods=['POST'])
@response(template_file='account/remove_pin.html')
def remove_pin_post():
    vm = RemovePinViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    pin = delete_pin(vm.pin_id)
    if not pin:
        vm.error = 'Pin could not be removed'
        return vm.to_dict()

    audit_message = 'Removed Pin ' + str(pin.WaypointsID) + ' from Mission ' + str(pin.MissionID)
    vm.message = 'Success! Removed Pin ' + str(pin.WaypointsID) + ' from Mission ' + str(pin.MissionID)
    vm.update()
    audit_log = audit_entry(vm.user_id, audit_message)
    if audit_log:
        vm.message = vm.message + '. This entry has been logged'
    return vm.to_dict()


########################## REMOVE TARGET ##########################


@blueprint.route('/account/remove_target', methods=['GET'])
@response(template_file='account/remove_target.html')
def remove_target_get():
    vm = RemoveTargetViewModel()

    if not vm.user_id:
        return flask.redirect('/account/login')
    return vm.to_dict()


@blueprint.route('/account/remove_target', methods=['POST'])
@response(template_file='account/remove_target.html')
def remove_target_post():
    vm = RemoveTargetViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    target = delete_target(vm.target_id)
    if not target:
        vm.error = 'Target could not be removed'
        return vm.to_dict()

    audit_message = 'Removed Target ' + str(target.TargetsID) + ' from Mission ' + str(target.MissionID)
    vm.message = 'Success! Removed Target ' + str(target.TargetsID) + ' from Mission ' + str(target.MissionID)
    vm.update()
    audit_log = audit_entry(vm.user_id, audit_message)
    if audit_log:
        vm.message = vm.message + '. This entry has been logged'
    return vm.to_dict()


########################## REMOVE MISSION ##########################


@blueprint.route('/account/remove_mission', methods=['GET'])
@response(template_file='account/remove_mission.html')
def remove_mission_get():
    vm = RemoveMissionViewModel()

    if not vm.user_id:
        return flask.redirect('/account/login')
    return vm.to_dict()


@blueprint.route('/account/remove_mission', methods=['POST'])
@response(template_file='account/remove_mission.html')
def remove_mission_post():
    vm = RemoveMissionViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    mission = delete_mission(vm.mission_id)
    if not mission:
        vm.error = 'Mission could not be removed'
        return vm.to_dict()

    audit_message = 'Removed Mission ' + str(mission.Number)
    vm.message = 'Success! Removed Mission ' + str(mission.Number)
    vm.update()
    audit_log = audit_entry(vm.user_id, audit_message)
    if audit_log:
        vm.message = vm.message + '. This entry has been logged'
    return vm.to_dict()


########################## REMOVE DIVE ##########################


@blueprint.route('/account/remove_dive', methods=['GET'])
@response(template_file='account/remove_dive.html')
def remove_dive_get():
    vm = RemoveDiveViewModel()

    if not vm.user_id:
        return flask.redirect('/account/login')
    return vm.to_dict()


@blueprint.route('/account/remove_dive', methods=['POST'])
@response(template_file='account/remove_dive.html')
def remove_dive_post():
    vm = RemoveDiveViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    dive = delete_dive(vm.dive_id)
    if not dive:
        vm.error = 'Mission could not be removed'
        return vm.to_dict()

    audit_message = 'Removed dive' + str(dive.DiveInfoID)
    vm.message = 'Success! Removed dive ' + str(dive.DiveInfoID)
    vm.update()
    audit_log = audit_entry(vm.user_id, audit_message)
    if audit_log:
        vm.message = vm.message + '. This entry has been logged'
    return vm.to_dict()

########################## REMOVE MANY DIVES ##########################


@blueprint.route('/account/remove_multiple_dives', methods=['GET'])
@response(template_file='account/remove_multiple_dives.html')
def remove_multiple_dives_get():
    vm = RemoveMultipleDivesViewModel()

    if not vm.user_id:
        return flask.redirect('/account/login')
    return vm.to_dict()


@blueprint.route('/account/remove_multiple_dives', methods=['POST'])
@response(template_file='account/remove_multiple_dives.html')
def remove_multiple_dives_post():
    vm = RemoveMultipleDivesViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    dive = delete_multiple_dives(vm.glider_id)
    if not dive:
        vm.error = 'Dives could not be removed'
        return vm.to_dict()

    audit_message = 'Removed dives glider' + str(dive.GliderID)
    vm.message = 'Success! Removed dives from SG' + str(dive.GliderID) + \
                 ' in Mission 1 <br> now go and delete the matlab lock files and dive images on the basestation:'\
                 + f'<br> /home/matlab/processed/sg{str(dive.GliderID)}/processed.1-x' + \
                 '<br> /mnt/gliderstore/dives/Mission1/' + str(dive.GliderID)
    vm.update()
    audit_log = audit_entry(vm.user_id, audit_message)
    if audit_log:
        vm.message = vm.message + '<br>This entry has been logged'
    return vm.to_dict()

########################## ASSIGN GLIDER ##########################


@blueprint.route('/account/assign_glider', methods=['GET'])
@response(template_file='account/assign_glider.html')
def assignglider_get():
    vm = AssignGliderViewModel()

    if not vm.user_id:
        return flask.redirect('/account/login')
    return vm.to_dict()


@blueprint.route('/account/assign_glider', methods=['POST'])
@response(template_file='account/assign_glider.html')
def assignglider_post():
    vm = AssignGliderViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()
    glider = assign_glider(vm.glider_num, vm.missionid)
    if not glider:
        vm.error = 'The glider could not be assigned to the mission'
        return vm.to_dict()

    audit_message = 'Assign glider SG' + str(vm.glider_num) + ' to mission' + str(vm.missionid)
    vm.message = 'Success! You have assigned glider ' '<a href="/gliders/SG' + str(vm.glider_num) + '">' + "SG" + str(
        vm.glider_num) + "</a>"  ' to ' + '<a href="/mission' + str(vm.missionid) + '">' + "mission " + str(vm.missionid) + "</a>"
    vm.glider_num = ''
    vm.missionid = ''
    audit_log = audit_entry(vm.user_id, audit_message)
    if audit_log:
        vm.message = vm.message + '. This entry has been logged'
    return vm.to_dict()

########################## ASSIGN TAG ##########################


@blueprint.route('/account/assign_tag', methods=['GET'])
@response(template_file='account/assign_tag.html')
def assigntag_get():
    vm = AssignTagViewModel()

    if not vm.user_id:
        return flask.redirect('/account/login')
    return vm.to_dict()


@blueprint.route('/account/assign_tag', methods=['POST'])
@response(template_file='account/assign_tag.html')
def assigntag_post():
    vm = AssignTagViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()
    tag = db_edits.assign_tag(vm.tag_num, vm.missionid, vm.gliderid)
    if not tag:
        vm.error = 'The tag could not be assigned'
        return vm.to_dict()

    audit_message = 'Add tag' + str(vm.tag_num)
    vm.message = f'Success! You have assigned tag {vm.tag_num} to SG{vm.gliderid} on mission {vm.missionid} '
    vm.tag_num = ''
    vm.missionid = ''
    vm.gliderid = ''
    audit_log = audit_entry(vm.user_id, audit_message)
    if audit_log:
        vm.message = vm.message + '. This entry has been logged'
    return vm.to_dict()

import flask
from ueaglider.infrastructure.view_modifiers import response
from ueaglider.services import user_service, db_edits
from ueaglider.infrastructure import cookie_auth as cookie_auth
from ueaglider.services.db_edits import audit_entry
from ueaglider.viewmodels.account.edit_viewmodel import AddWaypointViewModel
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


@blueprint.route('/account/add_waypoint', methods=['GET'])
@response(template_file='account/add_waypoint.html')
def addwaypoint_get():
    vm = AddWaypointViewModel()

    if not vm.user_id:
        return flask.redirect('/account/login')
    return vm.to_dict()


@blueprint.route('/account/add_waypoint', methods=['POST'])
@response(template_file='account/add_waypoint.html')
def addwaypoint_post():
    vm = AddWaypointViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    waypoint = db_edits.create_waypoint(vm.missionid, vm.name, vm.lat, vm.lon, vm.info)

    if not waypoint:
        vm.error = 'The waypoint could not be created'
        return vm.to_dict()

    audit_message = 'Add Waypoint ' + vm.name + ' to mission ' + str(vm.missionid)
    vm.message = 'Success! You have added Waypoint ' + vm.name + ' to mission ' + str(vm.missionid)
    vm.name = ''
    vm.missionid = ''
    vm.lat = ''
    vm.lon = ''
    vm.info = ''
    audit_log = audit_entry(vm.user_id, audit_message)
    if audit_log:
        vm.message = vm.message + '. This entry has been logged'
    #resp = flask.redirect('/account')
    return vm.to_dict()

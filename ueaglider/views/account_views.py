import flask
from ueaglider.infrastructure.view_modifiers import response

blueprint = flask.Blueprint('account', __name__, template_folder='templates')


@blueprint.route('/account/index')
@response(template_file='account/index.html')
def account_options():
    return {
        'value': None
    }


@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    return {
        'value': None
    }


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    return {
        'value': None
    }


@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    return {
        'value': None
    }


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    return {
        'value': None
    }

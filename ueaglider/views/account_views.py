import flask
from ueaglider.infrastructure.view_modifiers import response

blueprint = flask.Blueprint('account', __name__, template_folder='templates')


@blueprint.route('/account')
@response(template_file='account/index.html')
def account_options():
    return {
    }


@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():

    return {
    }


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    r = flask.request
    print(r.form)
    name = r.form.get('name')
    secret = r.form.get('secret', '').lower().strip()
    password = r.form.get('password').strip()
    if not name or not secret or not password:
        return {
            'name': name,
            'secret': secret,
            'password': password,
            'error': 'better fill all those fields boyo'}
    return {
    }


@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    return {
    }


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    return {
    }

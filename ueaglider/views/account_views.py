import flask
from ueaglider.infrastructure.view_modifiers import response
from ueaglider.services import user_service

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
    name = r.form.get('name')
    email = r.form.get('email', '').lower().strip()
    secret = r.form.get('secret', '').lower().strip()
    password = r.form.get('password').strip()
    if not name or not email or not secret or not password:
        return {
            'name': name,
            'secret': secret,
            'email': email,
            'password': password,
            'error': 'better fill all those fields boyo'}
    if secret != 'please':
        return {
            'name': name,
            'secret': secret,
            'email': email,
            'password': password,
            'error': "You didn't say the magic word"}
    user = user_service.create_user(name, email, password)
    if not user:
        return {
            'name': name,
            'secret': secret,
            'email': email,
            'password': password,
            'error': "A user with that email is already registered"}
    return flask.redirect('/account')


@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    return {
    }


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    r = flask.request
    email = r.form.get('email', '').lower().strip()
    password = r.form.get('password').strip()
    if not email or not password:
        return {
            'email': email,
            'password': password,
            'error': 'better fill all those fields boyo'}
    user = user_service.login_user(email, password)
    if not user:
        return {
            'email': email,
            'password': password,
            'error': 'email not registered or password does not match'}

    return flask.redirect('/account')

import flask
from ueaglider.infrastructure.view_modifiers import response
from ueaglider.services import user_service
from ueaglider.infrastructure import cookie_auth as cookie_auth

blueprint = flask.Blueprint('account', __name__, template_folder='templates')


@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    user_id = cookie_auth.get_user_id_via_auth_cookie(flask.request)
    if user_id is None:
        return flask.redirect('/account/login')
    user = user_service.find_user_by_id(user_id)
    if not user:
        return flask.redirect('/account/login')
    return {
        'user': user,
        'user_id': cookie_auth.get_user_id_via_auth_cookie(flask.request),

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
    resp = flask.redirect('/account')
    cookie_auth.set_auth(resp, user.UserID)
    return resp


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

    resp = flask.redirect('/account')
    cookie_auth.set_auth(resp, user.UserID)
    return resp


@blueprint.route('/account/logout')
def logout():
    resp = flask.redirect('/')
    cookie_auth.logout(resp)
    return resp


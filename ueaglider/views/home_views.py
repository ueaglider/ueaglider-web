import flask
from ueaglider.infrastructure.view_modifiers import response
from ueaglider.viewmodels.home.index_viewmodel import IndexViewModel
from ueaglider.viewmodels.home.sitemap_viewmodel import SiteMapViewModel

blueprint = flask.Blueprint('home', __name__, template_folder='templates')


@blueprint.route('/')
@response(template_file='home/index.html')
def index():
    """
    Home page method,
    :returns: counts of total missions, unique gliders and dives completed
    """
    vm = IndexViewModel()
    return vm.to_dict()


@blueprint.route('/sitemap.xml')
@response(mimetype='application/xml', template_file='home/sitemap.html')
def sitemap():
    vm = SiteMapViewModel()
    return vm.to_dict()


@blueprint.route('/robots.txt')
@response(mimetype='text/plain', template_file='home/robots.txt')
def robots():
    return {}


@blueprint.route('/<string:nonsense>.php')
@response(template_file='home/old_home.html')
def old_php_index(nonsense:str):
    vm = IndexViewModel()
    return vm.to_dict()


@blueprint.route('/DIVES/<string:nonsense>.php')
@response(template_file='home/old_home.html')
def old_php_dives_index(nonsense:str):
    vm = IndexViewModel()
    return vm.to_dict()
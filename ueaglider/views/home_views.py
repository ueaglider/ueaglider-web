import flask
from ueaglider.infrastructure.view_modifiers import response
from ueaglider.viewmodels.home.index_viewmodel import IndexViewModel

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

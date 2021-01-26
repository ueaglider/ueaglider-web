import flask
from ueaglider.infrastructure.view_modifiers import response
from ueaglider.services import mission_service
from ueaglider.viewmodels.glider.glider_viewmodel import GliderListViewModel, GliderViewModel

blueprint = flask.Blueprint('glider', __name__, template_folder='templates')


@blueprint.route('/gliders')
@response(template_file='glider/gliders_list.html')
def gliders_list():
    """
    :return:
    list of all gliders and links to them
    """
    vm = GliderListViewModel()
    return vm.to_dict()



@blueprint.route('/gliders/SG<int:glider_num>')
@response(template_file='glider/glider.html')
def gliders(glider_num: int):
    """
    :param glider_num: the glider number e.g. SG637
    :return:
    info on the glider and its missions
    """
    missions_nums = mission_service.glider_nums()
    id_list = [y for x in missions_nums for y in x]
    if glider_num not in id_list:
        return flask.redirect('/gliders')

    vm = GliderViewModel(glider_num)
    return vm.to_dict()


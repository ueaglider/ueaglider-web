from flask import Response
from tests.test_client import  flask_app


def test_glider():
    # This test will break if SG510 is ever permanently retired from the fleet
    from ueaglider.views.glider_views import gliders
    with flask_app.test_request_context(path='/gliders/SG510'):
        resp: Response = gliders(510)
    assert resp.status_code == 200
    assert b'Orca' in resp.data


def test_non_existent_glider():
    from ueaglider.views.glider_views import gliders
    with flask_app.test_request_context(path='/gliders/SG123'):
        resp: Response = gliders(123)
    # Should redirect to gliders page, so we expect a 302
    assert resp.status_code == 302

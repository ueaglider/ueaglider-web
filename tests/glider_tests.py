import datetime
import unittest.mock
from flask import Response
from tests.test_client import flask_app


def test_package_details_success():
    # Arrange
    from ueaglider.views.glider_views import gliders
    from ueaglider.data.db_classes import Gliders

    test_glider = Gliders()
    test_glider.Number = '123'
    test_glider.Name = 'TestyMcTestFace'
    test_glider.Info = 'For test purposes only, do not submerge'
    test_glider.MissionID = 10

    # Act
    with unittest.mock.patch('ueaglider.services.glider_service.glider_info',
                             return_value=test_glider):
        with flask_app.test_request_context(path='/gliders/SG' + test_glider.Number):
            resp: Response = gliders(test_glider.Number)

    # Assert
    assert b'omura' in resp.data


def test_package_details_404(client):
    # Arrange
    bad_package_url = 'Iamnotaglider'

    # Act
    with unittest.mock.patch('ueaglider.services.glider_service.glider_info',
                             return_value=None):
        resp: Response = client.get(bad_package_url)

    assert resp.status_code == 404
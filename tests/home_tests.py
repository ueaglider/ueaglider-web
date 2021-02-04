from flask import Response

from tests.test_client import client, flask_app
from ueaglider.views import home_views


def test_int_homepage(client):
    # Check that the home page returns a 200 and has an expected string in it
    r: Response = client.get('/')
    assert r.status_code == 200
    assert b'UEA glider group' in r.data


def test_homepage_missions():
    # Check that the mission list has at least one item in it
    with flask_app.test_request_context(path='/'):
        r: Response = home_views.index()

    assert r.status_code == 200
    # noinspection PyUnresolvedReferences
    assert len(r.model.get('mission_list')) > 0

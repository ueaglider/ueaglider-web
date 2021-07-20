"""
This stub mostly copied from TalkPython course. Creates the client fixture for testing the Flask app
Also adds necessary stuff to path
"""
# noinspection PyPackageRequirements
import pytest

import sys
import os

container_folder = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..'
))
sys.path.insert(0, container_folder)

import ueaglider.app
from ueaglider.app import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    client = flask_app.test_client()

    # noinspection PyBroadException,PyUnusedLocal
    try:
        ueaglider.app.configure()
    except Exception as x:
        # print(x)
        pass

    ueaglider.app.configure()

    yield client
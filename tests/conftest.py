import pytest
import os, sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from driver import *

""" TEST CONSTANTS """

USERNAME = 'Admin'
PASSWORD = 'AdminAdmin'
DATABASE = 'demo'  # PLEASE FILL IT WITH SOME DATA FOR TESTING

""" -------------- """

@pytest.fixture(scope='module')
def vadmin_without_auth():
    pytest.USERNAME = USERNAME
    pytest.PASSWORD = PASSWORD
    yield VAdminAPI()


@pytest.fixture(scope='module')
def vadmin():
    pytest.USERNAME = USERNAME
    pytest.PASSWORD = PASSWORD
    pytest.DATABASE = DATABASE
    obj = VAdminAPI()
    obj.auth_by_username(USERNAME, PASSWORD)
    yield obj

import pytest
import os, sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from driver import *

""" TEST CONSTANTS """

HOST = 'http://84.201.138.2'
USERNAME = 'Admin'
PASSWORD = 'AdminAdmin'
DATABASE = 'demo'  # PLEASE FILL IT WITH SOME DATA FOR TESTING

""" -------------- """

@pytest.fixture(scope='module')
def vadmin_without_auth():
    pytest.USERNAME = USERNAME
    pytest.PASSWORD = PASSWORD
    yield VAdminAPI(HOST, DATABASE)


@pytest.fixture(scope='module')
def vadmin():
    pytest.USERNAME = USERNAME
    pytest.PASSWORD = PASSWORD
    pytest.DATABASE = DATABASE
    obj = VAdminAPI(HOST, DATABASE)
    obj.auth_by_username(USERNAME, PASSWORD)
    yield obj

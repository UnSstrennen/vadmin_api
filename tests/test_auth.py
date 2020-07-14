import pytest


def test_auth_by_username(vadmin_without_auth):
    vadmin_without_auth.auth_by_username(pytest.USERNAME, pytest.PASSWORD)
    assert vadmin_without_auth.token_type
    assert vadmin_without_auth.access_token

def test_auth_by_token(vadmin_without_auth):
    vadmin_without_auth.token_type = ''
    vadmin_without_auth.access_token = ''
    token = vadmin_without_auth.get_token(pytest.USERNAME, pytest.PASSWORD)
    vadmin_without_auth.auth_by_token(vadmin_without_auth.token_type, token)
    assert vadmin_without_auth.access_token == token

import pytest


def test_auth_by_username(vadmin_without_auth):
    vadmin_without_auth.auth_by_username(pytest.USERNAME, pytest.PASSWORD)
    from driver import headers
    assert headers['Authorization']

def test_auth_by_token(vadmin_without_auth):
    token = vadmin_without_auth.get_token(pytest.USERNAME, pytest.PASSWORD)
    from driver import token_type
    vadmin_without_auth.auth_by_token(token_type, token)
    from driver import headers
    assert headers['Authorization'].split()[-1] == token

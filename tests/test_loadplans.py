import pytest


def test_get_load_plans(vadmin):
    res = vadmin.get_load_plans(pytest.DATABASE)
    assert type(res) is list
    assert res

def test_get_load_plan(vadmin):
    res = vadmin.get_load_plan(pytest.DATABASE, 1)
    assert res.id == 1

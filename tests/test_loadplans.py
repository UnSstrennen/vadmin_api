import pytest
from requests import HTTPError


def test_get_load_plans(vadmin):
    res = vadmin.get_load_plans(pytest.DATABASE)
    assert type(res) is list
    assert res

def test_get_load_plan(vadmin):
    res = vadmin.get_load_plan(pytest.DATABASE, 1)
    assert res.id == 1
    with pytest.raises(HTTPError):
        assert vadmin.get_load_plan('roowoo', 1)
        assert vadmin.get_load_plan(pytest.DATABASE, 100500)

def test_get_steps(vadmin):
    plan = vadmin.get_load_plan(pytest.DATABASE, 1)
    assert plan.get_steps()

def test_get_status(vadmin):
    plan = vadmin.get_load_plan(pytest.DATABASE, 1)
    assert plan.get_status()

def test_get_progress(vadmin):
    plan = vadmin.get_load_plan(pytest.DATABASE, 1)
    assert plan.get_progress() is not None

def test_start(vadmin):
    plan = vadmin.get_load_plan(pytest.DATABASE, 1)
    plan.start()
    assert plan.get_status() == 'Finished'
    broken_plan = vadmin.get_load_plan(pytest.DATABASE, 2)
    from driver import BrokenPlanError
    with pytest.raises(BrokenPlanError):
        assert broken_plan.start()

import pytest
from driver import BrokenPlanError
from requests import HTTPError
from time import sleep


def test_get_load_plans(vadmin):
    res = vadmin.get_load_plans()
    assert type(res) is list
    assert res

def test_get_load_plan_by_id(vadmin):
    res = vadmin.get_load_plan_by_id(1)
    assert res.id == 1
    with pytest.raises(HTTPError):
        assert vadmin.get_load_plan_by_id(1)
        assert vadmin.get_load_plan_by_id(100500)

def test_get_load_plan_by_name(vadmin):
    res = vadmin.get_load_plan_by_id(1)
    name = res.name
    res = vadmin.get_load_plan_by_name(name)
    assert res.name == name
    with pytest.raises(ValueError):
        assert vadmin.get_load_plan_by_name('barabashka123')

def test_get_steps(vadmin):
    plan = vadmin.get_load_plan_by_id(1)
    assert plan.get_status()

def test_get_progress(vadmin):
    plan = vadmin.get_load_plan_by_id(1)
    assert plan.get_progress() is not None

def test_execute(vadmin):
    plan = vadmin.get_load_plan_by_id(1)
    plan.execute()
    assert plan.get_status() == 'Finished'
    broken_plan = vadmin.get_load_plan_by_id(2)
    with pytest.raises(BrokenPlanError):
        assert broken_plan.execute()

def test_start(vadmin):
    plan = vadmin.get_load_plan_by_id(1)
    plan.start()
    assert plan.get_status() in ['Running', 'Finished']
    sleep(1)
    plan = vadmin.get_load_plan_by_id(2)
    with pytest.raises(BrokenPlanError):
        plan.start()

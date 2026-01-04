import os
import pytest
from model.explorer import Explorer
from errors import Duplicate, Missing

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import explorer, init


@pytest.fixture(scope="module")
def init_db():
    init.get_db()


@pytest.fixture
def sample() -> Explorer:
    return Explorer(name="Valera", description="Test Explorer", country="RU")


def test_create(sample):
    resp = explorer.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = explorer.create(sample)


def test_get_one(sample):
    resp = explorer.get_one(sample.name)
    assert resp == sample


def test_get_one_missing():
    with pytest.raises(Missing):
        _ = explorer.get_one("absence_name")


def test_modify(sample):
    sample.country = "CN"
    resp = explorer.modify(sample)
    assert resp == sample


def test_modify_missing():
    some: Explorer = Explorer(
        name="Test",
        country="TT",
        description="Test Creature",
    )
    with pytest.raises(Missing):
        _ = explorer.modify(some)


def test_delete(sample):
    resp = explorer.delete(sample)
    with pytest.raises(Missing):
        _ = explorer.get_one(sample.name)


def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = explorer.delete(sample)

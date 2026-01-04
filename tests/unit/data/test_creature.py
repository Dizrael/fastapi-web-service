import os
import pytest
from model.creature import Creature
from errors import Duplicate, Missing

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import creature, init


@pytest.fixture(scope="module")
def init_db():
    init.get_db()


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="yeti",
        country="CN",
        area="Himalayas",
        description="Harmless Himalayan",
        aka="Abominable Snowman",
    )


def test_create(sample):
    resp = creature.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = creature.create(sample)


def test_get_one(sample):
    resp = creature.get_one(sample.name)
    assert resp == sample


def test_get_one_missing():
    with pytest.raises(Missing):
        _ = creature.get_one("absence_name")


def test_modify(sample):
    sample.area = "Sesame Street"
    resp = creature.modify(sample)
    assert resp == sample


def test_modify_missing():
    some: Creature = Creature(
        name="Test",
        country="TT",
        area="",
        description="Test Creature",
        aka="TEST",
    )
    with pytest.raises(Missing):
        _ = creature.modify(some)


def test_delete(sample):
    resp = creature.delete(sample)
    with pytest.raises(Missing):
        _ = creature.get_one(sample.name)


def test_delete_missing(sample):
    sample.name = "NewTestName"
    with pytest.raises(Missing):
        _ = creature.delete(sample)

from src.model.creature import Creature
from src.service import creature as code

sample = Creature(
    name="Leshiy", aka="Lesnoy Straj", country="RU", area="Tayga", description="Zlobniy Mag Druid v vide dereva"
)


def test_create():
    resp = code.create(sample)
    assert resp == sample


def test_get_exists():
    resp = code.get_one("Leshiy")
    assert resp == sample


def test_get_missing():
    resp = code.get_one("bubblegum")
    assert resp is None

from src.model.creature import Creature
import src.fake.creature as data


def get_all() -> list[Creature]:
    return data.get_all()


def get_one(name) -> Creature | None:
    return data.get_one(name)


def create(creature: Creature) -> Creature:
    return data.create(creature)


def replace(id: int, creature: Creature) -> Creature:
    return data.replace(id, creature)


def modify(id, creature: Creature) -> Creature:
    return data.modify(id, creature)


def delete(id, creature: Creature) -> bool:
    return data.delete(id)

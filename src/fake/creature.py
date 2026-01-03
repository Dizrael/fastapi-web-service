from src.model.creature import Creature


# фиктивные данные, пока не произойдет замена на реальную базу данных и SQL
_creatures = [
    Creature(
        name="Leshiy", aka="Lesnoy Straj", country="RU", area="Tayga", description="Zlobniy Mag Druid v vide dereva"
    ),
    Creature(name="Rusalka", description="Krasivaya polu-jenshina polu-riba", country="KZ", area="*", aka="Ruslanka"),
]


def get_all() -> list[Creature]:
    """Возврат всех существ"""
    return _creatures


def get_one(name: str) -> Creature | None:
    """Возврат одного существа"""
    for _creature in _creatures:
        if _creature.name == name:
            return _creature
    return None


# Приведенные ниже варианты пока не функциональны,
# поэтому они просто делают вид, что работают,
# не изменяя реальный фиктивный список
def create(creature: Creature) -> Creature:
    """Добавление существа"""
    return creature


def modify(id: int, creature: Creature) -> Creature:
    """Частичное изменение записи существа"""
    return creature


def replace(id: int, creature: Creature) -> Creature:
    """Полная замена записи существа"""
    return creature


def delete(id: int) -> bool:
    """Удаление записи существа; возврат значения None,
    если запись существовала"""
    return None

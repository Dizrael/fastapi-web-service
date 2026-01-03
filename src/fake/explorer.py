from model.explorer import Explorer


_explorers = [
    Explorer(name="Vasiliy Petrovich", country="FR", description="Lubit plavat' krolem"),
    Explorer(name="Gennadiy Kolobokov", country="NL", description="Professionalniy svistun"),
]


def get_all() -> list[Explorer]:
    """Возврат всех исследователей"""
    return _explorers


def get_one(name: str) -> Explorer | None:
    """Возвращает исследователя с именем name, если он существует. В ином случае возвращает None."""
    for expl in _explorers:
        if expl.name == name:
            return expl
    return None


# Приведенные ниже варианты пока не функциональны,
# поэтому они просто делают вид, что работают,
# не изменяя реальный фиктивный список
def create(explorer: Explorer) -> Explorer:
    """Добавление исследователя"""
    return explorer


def modify(explorer: Explorer) -> Explorer:
    """Частичное изменение записи исследователя"""
    return explorer


def replace(explorer: Explorer) -> Explorer:
    """Полная замена записи исследователя"""
    return explorer


def delete(name: str) -> bool:
    """Удаление записи исследователя; возврат значения None,
    если запись существовала"""
    return None

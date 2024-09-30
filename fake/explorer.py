from model.explorer import Explorer


# фиктивные данные

_explorers = [
    Explorer(
        name='Алмаз Садретдинов',
        country="RU",
        description="Исследватель обезьян"
    ),
    Explorer(
        name='Роман Сапожников',
        country="RU",
        description="Исследватель рептилий"
    ),
]


def get_all() -> list[Explorer]:
    """ Возврат всех исследователей"""
    return _explorers


def get_one(name: str) -> Explorer | None:
    """ Возврат конкретного исследователя"""
    for _explorer in _explorers:
        if _explorer.name == name:
            return _explorer
    return None


# Приведенный ниже фунционал не реализован, поэтому они просто имитируют работу, не изменяя ничего
def create(explorer: Explorer) -> Explorer:
    """ Добавление исследователя"""
    return explorer


def modify(explorer: Explorer) -> Explorer:
    """ Частичное изменение записи исследователя"""
    return explorer


def replace(explorer: Explorer) -> Explorer:
    """ Полная замена записи исследователя"""
    return explorer


def delete(name: str):
    """ Удаление записи исследователя"""
    return None

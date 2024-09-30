from model.creature import Creature

# фиктивные данные

_creatures = [
    Creature(
        name='Йетти',
        aka='Снежный человек',
        country="CN",
        area='Гималаи',
        description="Король Гималаев"
    ),
    Creature(
        name='БигФут',
        aka='Большие ноги',
        country="RU",
        area='*',
        description="Дружит с йетти"
    ),
]


def get_all() -> list[Creature]:
    """ Возврат всех существ"""
    return _creatures


def get_one(name: str) -> Creature | None:
    """ Возврат конкретного существа"""
    for _creature in _creatures:
        if _creature.name == name:
            return _creature
    return None


# Приведенный ниже фунционал не реализован, поэтому они просто имитируют работу, не изменяя ничего
def create(creature: Creature) -> Creature:
    """ Добавление существа"""
    return creature


def modify(creature: Creature) -> Creature:
    """ Частичное изменение записи существа"""
    return creature


def replace(creature: Creature) -> Creature:
    """ Полная замена записи существа"""
    return creature


def delete(name: str):
    """ Удаление записи существа"""
    return None

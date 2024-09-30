import os
import pytest
from model.creature import Creature
from errors import Missing, Duplicate

os.environ["ANIMALS_SQLITE_DB"] = ":memory:"

from data import creature


@pytest.fixture()
def sample() -> Creature:
    return Creature(name="Тестовое животное",
                    country='Тестовая страна',
                    area='Тестовое обитание',
                    description='Тестовое описание',
                    aka='Тестовая кличка')


def test_create(sample):
    resp = creature.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = creature.create(sample)


def test_get_one(sample):
    resp = creature.get_one(sample.name)
    assert resp == sample


def test_get_one_missing(sample):
    with pytest.raises(Missing):
        _ = creature.get_one("Несуществующее животное")


def test_modify(sample):
    creature.area = "Sesame Street"
    resp = creature.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing():
    thing: Creature = Creature(name='Несуществующее животное', country='RU', area='', description='', aka='')
    with pytest.raises(Missing):
        _ = creature.modify(thing.name, thing)


def test_delete(sample):
    resp = creature.delete(sample)
    assert resp is True


def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = creature.delete(sample)

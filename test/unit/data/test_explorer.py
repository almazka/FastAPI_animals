import os
import pytest
from model.explorer import Explorer
from errors import Missing, Duplicate

os.environ["ANIMALS_SQLITE_DB"] = ":memory:"

from data import explorer


@pytest.fixture()
def sample() -> Explorer:
    return Explorer(name="Тестовый исследователь",
                    country='Тестовая страна',
                    description='Тестовое описание')


def test_create(sample):
    resp = explorer.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = explorer.create(sample)


def test_get_one(sample):
    resp = explorer.get_one(sample.name)
    assert resp == sample


def test_get_one_missing(sample):
    with pytest.raises(Missing):
        _ = explorer.get_one("Несуществующий исследователь")


def test_modify(sample):
    explorer.description = "Изменение описания"
    resp = explorer.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing():
    thing: Explorer = Explorer(name='Несуществующий исследватель', country='RU', description='')
    with pytest.raises(Missing):
        _ = explorer.modify(thing.name, thing)


def test_delete(sample):
    resp = explorer.delete(sample)
    assert resp is True


def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = explorer.delete(sample)

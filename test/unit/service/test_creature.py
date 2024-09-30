from model.creature import Creature
from service import creature as code


sample = Creature(name="Тестовое животное",
                  country='Тестовая страна',
                  area='Тестовое обитание',
                  description='Тестовое описание',
                  aka='Тестовая кличка')


def test_create():
    resp = code.create(sample)
    assert resp == sample


def test_get_exist():
    resp = code.get_one('Тестовое животное')
    assert resp == sample


def test_get_missing():
    resp = code.get_one("Несуществующее животное")
    assert resp is True

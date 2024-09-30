from .init import curs, IntegrityError
from model.creature import Creature
from errors import Missing, Duplicate


SQL_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS creature(name text PRIMARY KEY,
                                                          description text,
                                                          country text, 
                                                          area text,
                                                          aka text)"""

curs.execute(SQL_CREATE_TABLE)


def row_to_model(row: tuple) -> Creature:
    name, description, country, area, aka = row
    return Creature(name=name, description=description, country=country, area=area, aka=aka)


def model_to_dict(creature: Creature) -> dict:
    return creature.dict()


def get_one(name: str) -> Creature:
    query = 'SELECT * FROM creature WHERE name=:name'
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Creature {name} not found")


def get_all() -> list[Creature]:
    query = 'SELECT * FROM creature'
    curs.execute(query)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]


def create(creature: Creature) -> Creature:
    query = 'INSERT INTO creature values (:name, :description, :country, :area, :aka)'
    params = model_to_dict(creature)
    try:
        curs.execute(query, params)
    except IntegrityError:
        raise Duplicate(msg=f"Creature {creature.name} already exist")
    return get_one(creature.name)


def modify(name: str, creature: Creature) -> Creature:
    query = """UPDATE creature SET country=:country,
                                   name=:name,
                                   description=:description,
                                   area=:area,
                                   aka=:aka
                                WHERE name=:name_orig"""
    params = model_to_dict(creature)
    params["name_orig"] = name
    curs.execute(query, params)
    if curs.rowcount == 1:
        return get_one(creature.name)
    else:
        raise Missing(msg=f"Creature {creature.name} not found")


def delete(creature: Creature) -> bool:
    query = 'DELETE FROM creature WHERE name = :name'
    params = {"name": creature.name}
    res = curs.execute(query, params)
    if res.rowcount != 1:
        raise Missing(msg=f"Creature {creature.name} not found")
    return bool(res)


from .init import curs, IntegrityError
from model.explorer import Explorer
from errors import Missing, Duplicate

SQL_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS explorer(name text PRIMARY KEY,
                                                          description text,
                                                          country text)"""

curs.execute(SQL_CREATE_TABLE)


def row_to_model(row: tuple) -> Explorer:
    name, description, country = row
    return Explorer(name=name, description=description, country=country)


def model_to_dict(explorer: Explorer) -> dict:
    return explorer.dict() if explorer else None


def get_one(name: str) -> Explorer:
    query = 'SELECT * FROM explorer WHERE name=:name'
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Explorer {name} not found")


def get_all() -> list[Explorer]:
    query = 'SELECT * FROM explorer'
    curs.execute(query)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]


def create(explorer: Explorer) -> Explorer:
    query = 'INSERT INTO explorer values (:name, :description, :country)'
    params = model_to_dict(explorer)
    try:
        curs.execute(query, params)
    except IntegrityError:
        raise Duplicate(msg=f"Explorer {explorer.name} already exist")
    return get_one(explorer.name)


def modify(name: str, explorer: Explorer) -> Explorer:
    query = """UPDATE explorer SET country=:country,
                                   name=:name,
                                   description=:description
                                WHERE name=:name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = name
    curs.execute(query, params)
    if curs.rowcount == 1:
        return get_one(explorer.name)
    else:
        raise Missing(msg=f"Explorer {explorer.name} not found")


def delete(explorer: Explorer) -> bool:
    query = 'DELETE FROM explorer WHERE name = :name'
    params = {"name": explorer.name}
    res = curs.execute(query, params)
    if res.rowcount != 1:
        raise Missing(msg=f"Explorer {explorer.name} not found")
    return bool(res)

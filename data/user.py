from model.user import User
from .init import curs, IntegrityError
from errors import Missing, Duplicate

SQL_CREATE_TABLE_USER = """CREATE TABLE IF NOT EXISTS user(
                                name text primary key,
                                hash text)"""

SQL_CREATE_TABLE_XUSER = """CREATE TABLE IF NOT EXISTS xuser(
                                name text primary key,
                                hash text)"""

curs.execute(SQL_CREATE_TABLE_USER)
curs.execute(SQL_CREATE_TABLE_XUSER)


def row_to_model(row: tuple) -> User:
    name, hash = row
    return User(name=name, hash=hash)


def model_to_dict(user: User) -> dict:
    return user.dict()


def get_one(name: str) -> User:
    query = """SELECT * FROM user WHERE name=:name"""
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"User {name} not found")


def get_all() -> list[User]:
    query = """SELECT * FROM USER"""
    curs.execute(query)
    return [row_to_model(row) for row in curs.fetchall()]


def create(user: User, table: str = "user"):
    """ Добавление пользовател в таблицу user или xuser"""
    query = f"""INSERT INTO {table} (name, hash) VALUES (:name, :hash)"""
    params = model_to_dict(user)
    try:
        curs.execute(query, params)
    except IntegrityError:
        raise Duplicate(msg=f"{table}: user {user.name} already exist")


def modify(name: str, user: User) -> User:
    query = """UPDATE user SET name=:name, hash=:hash WHERE name=:name0"""
    params = {"name": user.name, "hash": user.hash, "name0": name}
    curs.execute(query, params)
    if curs.rowcount == 1:
        return get_one(user.name)
    else:
        raise Missing(msg=f"User {name} not found")


def delete(name: str) -> None:
    """ Удаление пользователя из таблиц user и добавление в таблицу xuser"""
    user = get_one(name)
    query = """DELETE FROM user WHERE name=:name"""
    params = {"name": name}
    curs.execute(query, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"User {name} not found")
    create(user, table='xuser')

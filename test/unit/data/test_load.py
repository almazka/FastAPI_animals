from faker import Faker
from time import perf_counter


def load():
    from errors import Duplicate
    from data.explorer import create
    from model.explorer import Explorer
    f = Faker()
    num = 100000
    t1 = perf_counter()
    for row in range(num):
        try:
            create(Explorer(name=f.name(), country=f.country(), description=f.address()))
        except Duplicate:
            pass

    t2 = perf_counter()
    print(num, "rows")
    print("Write time: ", t2-t1)


def read_db():
    from data.explorer import get_all

    t1 = perf_counter()
    _ = get_all()
    t2 = perf_counter()
    print("db read time: ", t2-t1)


def read_api():
    from fastapi.testclient import TestClient
    from main import app

    t1 = perf_counter()
    client = TestClient(app)

    _ = client.get("/explorer/")
    t2 = perf_counter()
    print("Read api time: ", t2-t1)


load()
read_db()
read_db()
read_api()

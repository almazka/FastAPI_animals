from pydantic import BaseModel


class Creature(BaseModel):
    """ Базовый класс существо"""
    name: str
    country: str
    area: str
    description: str
    aka: str

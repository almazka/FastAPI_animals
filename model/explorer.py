from pydantic import BaseModel


class Explorer(BaseModel):
    """ Базовый класс Исследователи"""
    name: str
    country: str
    description: str

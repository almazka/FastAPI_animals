import os
from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model.user import User

if os.getenv("ANIMALS_UNIT_TEST"):
    from fake import user as service
else:
    from service import user as service

from errors import Missing, Duplicate

ACCESS_TOKEN_EXPIRES_MINUTES = 30

router = APIRouter(prefix="/user")


oauth2_dep = OAuth2PasswordBearer(tokenUrl='token')


def unauthorized():
    raise HTTPException(
        status_code=401,
        detail="Incorrect Username or Password",
        headers={"WWW-Authenticate": "Bearer"})


@router.post("/token")
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """ Получение имени пользователя и пароля из формы Oauth и возврат токена доступа"""
    user = service.auth_user(form_data.username, form_data.password)
    if not user:
        unauthorized()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = service.create_access_token(info={"sub": user.name}, expires=expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    """ Возврат текущего токена доступа"""
    return {'token': token}


@router.get("/")
def get_all() -> list[User]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> User:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("/", status_code=201)
def create(user: User) -> User:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.patch("/")
def modify(name: str, user: User) -> User:
    try:
        return service.modify(name, user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete('/{name}')
def delete(name: str) -> None:
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

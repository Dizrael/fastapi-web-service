import os
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from model.user import User
if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import user as service
else:
    from service import user as service
from errors import Missing, Duplicate

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/user")

# Эта зависимость создает сообщение в каталоге "/user/token" (из формы с именем пользователя и паролем)
# и возвращает токен доступа.
oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")

def unauthed():
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Incorrect username of password",
        headers={"WWW-Authenticate": "Bearer"},
    )

# К этой конечной точке направляется любой вызов, содержащий зависимость oauth2_dep():
@router.post("/token")
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Получение имени пользователя и пароля из формы OAuth, возврат токена доступа"""
    user = service.auth_user(form_data.username, form_data.password)
    if not user:
        unauthed()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(data={'sub': user.name}, expires=expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    """Возврат текущего токена доступа"""
    return {"token": token}

@router.get("/")
def get_all() -> list[User]:
    return service.get_all()

@router.get("/{name}")
def get_one(name: str) -> User:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=exc.msg)


@router.post("/")
def create(user: User) -> User:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=exc.msg)


@router.patch("/")
def modify(name: str, user: User) -> User:
    try:
        return service.modify(name, user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{name}")
def delete(name: str) -> None:
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
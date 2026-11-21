from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.security.authentication import (
    Authentication,
    get_authenticated_user,
    get_authentication_service,
)
from app.security.models import Token
from app.users.models import UserModel

auth = APIRouter()


@auth.post("/login")
async def login_access_token(
    authService: Annotated[Authentication, Depends(get_authentication_service)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = authService.create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@auth.get("/test")
def test_hello_world(
    logged_user: Annotated[UserModel, Depends(get_authenticated_user)],
) -> str:
    return "Hello World!! " + logged_user.username

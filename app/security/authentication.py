from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from app.config import Settings, get_settings
from app.database.models import User
from app.users.models import UserModel

fake_users_db = {
    "Test_user": User(
        username="Test_user",
        fullname="Super Unuseful User",
        email="testing.user@testing.com",
        hashed_password="$argon2id$v=19$m=65536,t=3,p=4$WIq6s5MFnGNgKu/Jz/Qw0w$d7j/efZCPVFszjcF0KzJ0u4vRhUnJzU5DNQ+OMSWwvk",
    )
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Authentication:
    password_hash = PasswordHash.recommended()

    # DUMMY HASH
    #   Checks hash for unexisting users for security purposes.
    DUMMY_HASH = password_hash.hash("dummypassword")

    def __init__(self, settings: Settings):
        self._settings = settings

    def get_user(self, username: str) -> User | None:
        if username in fake_users_db:
            return fake_users_db[username]
        return None

    # PASSWORDS MANAGEMENT

    def verify_password(self, password: str, hashed_passworkd: str) -> bool:
        return self.password_hash.verify(password, hashed_passworkd)

    def get_password_hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    def authenticate_user(self, username: str, password: str) -> UserModel | None:
        """
        function authenticate_user: Verify username and password
            @username: username to verify
            @password: user password

            Return: UserModel object or None if not authorized. If the
                    user does not exist, verify the password with a dummy hash
                    for security reasons (same delay with both real user or wrong)
        """
        user: User | None = self.get_user(username=username)
        if not user:
            self.verify_password(password, self.DUMMY_HASH)
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return UserModel.model_validate(user.model_dump())

    # TOKEN MANAGEMENT

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        """
        function create_access_token: encode data on a JWT access token.
            @data: data to encode
            @expires_delta: timedelta of token expiration time (default is ACCESS_TOKEN_EXPIRE_DAYS)

            Return: return an access token generated with the data and expiration date encoded
                    with the key SECRET_KEY.
        """
        if expires_delta is None:
            expires_delta = timedelta(days=self._settings.access_token_expire_days)
        to_encode = data.copy()
        expiration = datetime.now(UTC) + expires_delta
        to_encode.update({"exp": expiration})

        return jwt.encode(
            to_encode,
            self._settings.secret_key,
            algorithm=self._settings.hash_algorithm,
        )

    def decode_access_token(self, token: str) -> UserModel | None:
        try:
            payload = jwt.decode(
                token,
                self._settings.secret_key,
                algorithms=[self._settings.hash_algorithm],
            )
            username = payload.get("sub")
            if username is None:
                return None

            user = self.get_user(username=username)
        except InvalidTokenError:
            return None

        if user is None:
            return None
        return UserModel.model_validate(user.model_dump())


def get_authentication_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Authentication:
    return Authentication(settings=settings)


# TODO: This functions shall be moved to autorization services
async def get_user_from_token(
    authService: Annotated[Authentication, Depends(get_authentication_service)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserModel:
    # Unauthorized exception
    unauth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = authService.decode_access_token(token=token)
    if user is None:
        raise unauth_exception

    return user


async def get_authenticated_user(
    active_user: Annotated[UserModel, Depends(get_user_from_token)],
) -> UserModel:
    if active_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return active_user

from sqlmodel import Field, SQLModel


class UserModel(SQLModel):
    username: str = Field(index=True)
    fullname: str
    email: str | None = Field(default=None, unique=True)
    disabled: bool | None = None


class User(UserModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

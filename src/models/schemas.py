from pydantic import (BaseModel)


class UserOut(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str
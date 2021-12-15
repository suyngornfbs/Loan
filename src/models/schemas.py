import datetime
from typing import Optional

from pydantic import (BaseModel)


class UserOut(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


# class UserInDB(UserOut):
#     hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class Login(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class CustomerToDB(BaseModel):
    id: Optional[int]
    cus_code: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    dob: Optional[datetime.date]
    phone: Optional[str]
    nationality: Optional[str]
    email: Optional[str]
    identity_type: Optional[str]
    identity_number: Optional[str]
    identity_date: Optional[str]
    id_card: Optional[str]
    street_no: Optional[str]
    address: Optional[str]
    status: Optional[str]
    profile_img: Optional[str]
    attachment_file: Optional[str]
    occupation: Optional[str]
    income: Optional[float]
    updated_by: Optional[int]
    created_by: Optional[int]
    crated_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]
    deleted_at: Optional[datetime.date]

    class Config:
        orm_mode = True

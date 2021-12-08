import datetime

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

    class Config:
        orm_mode = True


class CustomerToDB:
    cus_code: str
    first_name: str
    last_name: str
    gender: str
    dob: datetime.date
    phone: str
    nationality: str
    email: str
    identity_type: str
    identity_number: str
    identity_date: str
    id_card: str
    street_no: str
    address: str
    status: str
    profile_img: str
    attachment_file: str
    occupation: str
    income: float
    created_by: int
    updated_by: int
    crated_at: datetime.date
    updated_at: datetime.date
    deleted_at: datetime.date

    class Config:
        orm_mode = True

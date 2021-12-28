import datetime
from typing import Optional

from pydantic import (BaseModel)


class UserIn(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    dob: Optional[datetime.date]
    gender: Optional[str]
    con_password: Optional[str]

    class Config:
        orm_mode = True


# class UserUpdate(BaseModel):
#     name: Optional[str]
#     password: Optional[str]
#
#     class Config:
#         orm_mode = True


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


class CustomerIn(BaseModel):
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
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]
    deleted_at: Optional[datetime.date]

    class Config:
        orm_mode = True


class DisbursementIn(BaseModel):
    # dis_code: Optional[str]
    cus_id: int
    # gran_id: Optional[int]
    # col_id: Optional[int]
    # branch_id: Optional[int]
    # status: Optional[str]
    # product_type: Optional[str]
    repayment_method: str
    interest_rate: float
    balance: float
    # term: Optional[int]
    step: int
    duration: int
    # interest_term: Optional[int]
    # propose_amount: Optional[float]
    # approve_amount: Optional[float]
    # principal: float
    fee_rate: float
    dis_date: datetime.date
    first_date: datetime.date
    # purpose: Optional[str]
    # day_in_month: Optional[int]
    # day_in_year: Optional[int]
    # holiday_weekend: Optional[str]
    # contract_by: Optional[int]
    # created_by: Optional[int]
    # updated_by: Optional[int]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    # deleted_at: Optional[datetime.date]

    class Config:
        orm_mode = True


class ScheduleIn(BaseModel):
    cus_id: int
    dis_id: int
    collection_date: datetime.date
    collected_date: datetime.date
    status: str
    balance: float
    sch_no: int
    principal: float
    principal_paid: Optional[float]
    interest: float
    interest_paid: Optional[float]
    fee: float
    fee_paid: float
    penalty: Optional[float]
    penalty: Optional[float]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True

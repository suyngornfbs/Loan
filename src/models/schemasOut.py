import datetime
from typing import Optional

from pydantic import (BaseModel)


class UserOut(BaseModel):
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    gender: Optional[str]
    dob: Optional[datetime.date]

    class Config:
        orm_mode = True


class CustomerOut(BaseModel):
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
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]
    deleted_at: Optional[datetime.date]

    class Config:
        orm_mode = True


class DisbursementOut(BaseModel):
    id: Optional[int]
    dis_code: Optional[str]
    cus_id: Optional[int]
    # gran_id: Optional[int]
    # col_id: Optional[int]
    # branch_id: Optional[int]
    status: Optional[str]
    product_type: Optional[str]
    repayment_method: Optional[str]
    interest_rate: Optional[float]
    balance: Optional[float]
    term: Optional[int]
    step: Optional[int]
    duration: Optional[int]
    # interest_term: Optional[int]
    # propose_amount: Optional[float]
    # approve_amount: Optional[float]
    principal: Optional[float]
    fee_rate: Optional[float]
    dis_date: Optional[datetime.date]
    first_date: Optional[datetime.date]
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


class ScheduleOut(BaseModel):
    id: Optional[int]
    cus_id: Optional[int]
    dis_id: Optional[int]
    collection_date: Optional[datetime.date]
    collected_date: Optional[datetime.date]
    status: Optional[str]
    balance: Optional[float]
    sch_no: Optional[int]
    principal: Optional[float]
    principal_paid: Optional[float]
    interest: Optional[float]
    interest_pai: Optional[float]
    fee: Optional[float]
    fee_paid: Optional[float]
    penalty: Optional[float]
    penalty: Optional[float]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True

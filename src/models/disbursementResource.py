from typing import Optional
from pydantic import (BaseModel)
from datetime import date
from ..models.schemasOut import CustomerOut, ScheduleOut, DisbursementOut


class PaymentOut(BaseModel):
    principal: Optional[float]
    interest: Optional[float]
    fee: Optional[float]
    penalty: Optional[float]
    total: Optional[float]
    date: Optional[date]

    class Config:
        orm_mode = True


class PayIn(BaseModel):
    amount: Optional[float]

    class Config:
        orm_mode = True

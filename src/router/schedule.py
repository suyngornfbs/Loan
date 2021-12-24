from fastapi import APIRouter, Depends
from ..models.schemasIn import UserIn, PaidIn
from ..models.schemasOut import ScheduleOut
from pony.orm import db_session
from ..utils.payment import *
router = APIRouter()


@router.get('/disbursement/{id}/schedule', tags=['Schedule'])
def scheduleByLoan(id: int):
    with db_session:
        schedules = Model.Schedule.select(lambda s: s.dis_id == id)
        if schedules is not None:
            return [ScheduleOut.from_orm(s) for s in schedules]
        return {
            'message': 'disbursement or schedule not defined!'
        }

@router.post('/disbursement/{id}/payment', tags=['Schedule'])
def payment(id: int, request: PaidIn):
    strting = "Hello"
    payment = Payment(id, request)
    return payment.pay()

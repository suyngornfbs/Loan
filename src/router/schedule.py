from fastapi import APIRouter, Depends
from ..models.schemasIn import UserIn
from ..models.schemasOut import ScheduleOut, DisbursementOut, CustomerOut
from ..models.model import Model
from ..config.auth import get_current_user
from pony.orm import db_session
from datetime import date
from ..utils.disbursementUtil import *
from ..models.disbursementResource import PaymentOut, PayIn
from ..utils.ScheduleUtil import *

router = APIRouter()


@router.get('/disbursement/{id}/schedule', tags=['Schedule'])
def scheduleByLoan(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        schedules = Model.Schedule.select(lambda s: s.dis_id == id)
        if schedules:
            return [ScheduleOut.from_orm(s) for s in schedules]
        return {
            'message': 'disbursement or schedule not defined!'
        }


@router.get('/disbursement/{id}/form', tags=['Schedule'])
def loan_form(id: int):
    with db_session:
        disbursements_db = Model.Disbursement.get(lambda d: d.id == id)
        if not disbursements_db:
            return {
                'message': 'Disbursement is not found!'
            }
        customers_db = Model.Customer.get(lambda c: c.id == disbursements_db.cus_id)
        schedules_db = Model.Schedule.select(lambda s: s.dis_id == disbursements_db.id)

        data = {
            'disbursement': DisbursementOut.from_orm(disbursements_db),
            'customer': CustomerOut.from_orm(customers_db),
            'schedules': [ScheduleOut.from_orm(s) for s in schedules_db],
            'pay_now': paynow(disbursements_db.id),
            'pay_off': payOff(disbursements_db.id)
        }
        return {
            'data': data
        }


@router.post('/disbursement/{id}/schedule/paynow', tags=['Schedule'])
def pay_now(id: int, request: PayIn):
    with db_session:

        is_schedule = Model.Schedule.select(lambda s: s.dis_id == id)
        if not is_schedule:
            return {
                'message': 'Disbursement is not found!'
            }

        # schedules = Model.Schedule.select(lambda s: s.dis_id == id and s.status in ('Past Due', 'Due Today', 'Partial Paid', 'Partial Paid But Late'))
        # if schedules:
        schedules = Model.Schedule.select(
            lambda s: s.dis_id == id and s.status in ('Not Yet Due', 'Partial Paid', 'Past Due', 'Due Today',
                                                      'Partial Paid But Late')).first()
        while request.amount > 0:
            pay = getPayment(request.amount, schedules)
            updatePay(schedules, pay)
            request.amount = pay[3]
            disbursed = Model.Disbursement.get(lambda d: d.id == schedules.dis_id)
            if disbursed.status == 'Closed' and request.amount > 0:
                return {
                    'message': f'Payment successfully and You have {request.amount} $ left.'
                }
            sche_no = schedules.sch_no + 1
            schedules = Model.Schedule.select(lambda s: s.dis_id == id and s.sch_no == sche_no).first()

        return {
            'message': 'Payment successfully'
        }

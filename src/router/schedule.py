from fastapi import APIRouter, Depends
from ..models.schemasIn import UserIn
from ..models.schemasOut import ScheduleOut, DisbursementOut, CustomerOut
from ..models.model import Model
from ..config.auth import get_current_user
from pony.orm import db_session
from ..utils.disbursementUtil import *
from ..models.disbursementResource import PaymentOut, PayIn

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
            'pay_now': paynow(disbursements_db.id)
        }
        return {
            'data': data
        }


@router.post('/disbursement/{id}/schedule/paynow', tags=['Schedule'])
def pay_now(id: int, request: PayIn):
    with db_session:
        schedules = Model.Schedule.select(lambda s: s.dis_id == id and s.status == 'Not Yet Due').first()
        if not schedules:
            return {
                'message': 'Disbursement is not found!'
            }
        total = totalPayment(schedules, request.amount)
        if total == 1:
            schedules.status = 'Fully Paid On Time'
            schedules.principal_paid = schedules.principal
            schedules.interest_pai = schedules.interest
            schedules.fee_paid = schedules.fee
            schedules.penalty_paid = schedules.penalty
            schedules.collected_date = date.today()

            Model.SchedulePaid(
                sch_id=schedules.id,
                invoice=invoice(),
                paid_date=date.today(),
                payment_date=schedules.collection_date,
                interest_paid=schedules.interest_pai,
                penalty_paid=schedules.penalty_paid,
                fee_paid=schedules.fee_paid,
                status='Close',

            )

        return {
            'message': 'Payment successfully'
        }

from fastapi import APIRouter, Depends
from ..models.schemasIn import UserIn
from ..models.schemasOut import ScheduleOut, DisbursementOut, CustomerOut, SchedulePaidOut
from ..models.model import Model
from ..config.auth import get_current_user
from pony.orm import db_session
from datetime import date
from ..utils.disbursementUtil import *
from ..models.disbursementResource import PaymentOut, PayIn
from ..config.auth import get_current_user
from ..utils.ScheduleUtil import *

router = APIRouter()


@router.get('/disbursement/{id}/schedule', tags=['Schedule'])
def scheduleByLoan(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        schedules = Model.Schedule.select(lambda s: s.dis_id == id)
        if schedules:
            return {
                'success': 1,
                'data': [ScheduleOut.from_orm(s) for s in schedules]
            }
        return {
            'success': 0,
            'message': 'disbursement or schedule not defined!'
        }


@router.get('/disbursement/{id}/form', tags=['Schedule'])
def loan_form(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        disbursements_db = Model.Disbursement.get(lambda d: d.id == id)
        if not disbursements_db:
            return {
                'success': 0,
                'message': 'Disbursement is not found!'
            }
        customers_db = Model.Customer.get(lambda c: c.id == disbursements_db.cus_id)
        schedules_db = Model.Schedule.select(lambda s: s.dis_id == disbursements_db.id).order_by(lambda: s.id)

        data = {
            'disbursement': DisbursementOut.from_orm(disbursements_db),
            'customer': CustomerOut.from_orm(customers_db),
            'schedules': [getSchedule(s) for s in schedules_db],
            'total_sche': getTotalSche(disbursements_db.id),
            'pay_now': paynow(disbursements_db.id),
            'pay_off': payOff(disbursements_db.id)
        }
        return {
            'success': 1,
            'data': data
        }


@router.post('/disbursement/{id}/schedule/paynow', tags=['Schedule'])
def pay_now(id: int, request: PayIn, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        validation = checkDisbursedAndSchedule(id)
        if validation != "ok":
            return validation
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
                    'success': 1,
                    'message': f'Payment successfully and You have {request.amount} $ left.'
                }
            sche_no = schedules.sch_no + 1
            schedules = Model.Schedule.select(lambda s: s.dis_id == id and s.sch_no == sche_no).first()

        return {
            'success': 1,
            'message': 'Payment successfully'
        }


@router.post('/disbursement/{id}/schedule/payoff', tags=['Schedule'])
def payoff(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        validation = checkDisbursedAndSchedule(id)
        if validation != "ok":
            return validation
        disbursement = Model.Disbursement.get(lambda d: d.id == id)
        pay_off = payOff1(disbursement.id)
        schedules = Model.Schedule.select(
            lambda s: s.dis_id == id and s.status in ('Not Yet Due', 'Partial Paid', 'Past Due', 'Due Today',
                                                      'Partial Paid But Late')).first()
        schedules.interest = schedules.interest_paid = pay_off.get('interest')
        schedules.fee = schedules.fee_paid = pay_off.get('fee')
        schedules.principal = schedules.principal_paid = pay_off.get('principal')
        schedules.collected_date = date.today()
        schedules.status = "Paid Off"
        disbursement.status = "Paid Off"

        Model.SchedulePaid(
            dis_id=id,
            sch_id=schedules.id,
            invoice=invoice(),
            paid_date=date.today(),
            principal_paid=schedules.principal,
            payment_date=schedules.collection_date,
            interest_paid=schedules.interest_paid,
            penalty_paid=schedules.penalty_paid,
            fee_paid=schedules.fee_paid,
            status='Paid Off',
        )
        rm_sche = Model.Schedule.select(lambda s: s.sch_no > schedules.sch_no and s.dis_id == id)
        for rm in rm_sche:
            rm.delete()

        return {
            'success': 1,
            'message': 'Paid off was successful'
        }


@router.get('/disbursement/{id}/schedule-paid', tags=['Schedule'])
def schedule_paid(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        schedule_paids = Model.SchedulePaid.select(lambda s: s.dis_id == id)
        if not schedule_paids:
            return {
                'success': 0,
                'message': 'Disbursement or Schedule not found!'
            }
        return {
            'success': 1,
            'data': [getSchedulePaid(s) for s in schedule_paids]
        }

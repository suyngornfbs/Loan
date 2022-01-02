from fastapi import APIRouter, Depends
from pony.orm import *
from ..models.model import Model
from ..models.schemasIn import UserIn
from datetime import date
from dateutil.relativedelta import relativedelta
from ..config.auth import get_current_user

router = APIRouter()


@router.get('/dashboard', tags=['Dashboard'])
async def dashboard(current_user: UserIn = Depends(get_current_user)):
    with db_session:
        return {
            'success': 1,
            'data': {
                'customers': getAllCustomer(),
                'disbursement': getDisbursement(),
                'collection': getCollection(),
                'collected': getCollected()
            }
        }


def getAllCustomer():
    with db_session:
        customers = Model.Customer.select()

        counted = count(c for c in customers if getLastMonth() <= c.created_at <= getNextMonth())
        return counted


def getDisbursement():
    with db_session:
        disbursement = Model.Disbursement.select(
            lambda d: getLastMonth() <= d.dis_date and d.dis_date <= getNextMonth())
        return count(d for d in disbursement)


def getCollection():
    with db_session:
        schedule = Model.Schedule.select(
            lambda s: getLastMonth() <= s.collection_date and s.collection_date <= getNextMonth()
                      and s.sch_no != 0)
        principal = sum(s.principal for s in schedule if s.principal)
        interest = sum(s.interest for s in schedule if s.interest)
        fee = sum(s.fee for s in schedule if s.fee)
        return principal + interest + fee


def getCollected():
    with db_session:
        try:
            schedule_paid = Model.SchedulePaid.select(
                lambda s: getLastMonth() <= s.paid_date and s.paid_date <= getNextMonth())
            principal = sum(s.principal_paid for s in schedule_paid if s.principal_paid)
            interest = sum(s.interest_paid for s in schedule_paid if s.interest_paid)
            fee = sum(s.fee_paid for s in schedule_paid if s.fee_paid)
        except ValueError:
            pass
        return principal + interest + fee


def getLastMonth():
    return date.today().replace(day=1) - relativedelta(months=1)


def getNextMonth():
    return date.today().replace(day=1) + relativedelta(months=1)

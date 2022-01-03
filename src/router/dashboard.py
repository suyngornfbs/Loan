from fastapi import APIRouter, Depends
from pony.orm import *
from ..models.model import Model
from ..models.schemasIn import UserIn
from datetime import date
import datetime
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
                'customers_rate': getAllCustomerRate(),
                'disbursement': getDisbursement(),
                'disbursement_rate': getDisbursementRate(),
                'collection': getCollection(),
                'collection_rate': getCollectionRate(),
                'collected': getCollected(),
                'collected_rate': getCollectedRate(),
                'chart_collection': getChartCollection(),
                'chart_collected': getChartCollected()
            }
        }


def getAllCustomer():
    with db_session:
        customers = Model.Customer.select()
        counted = count(c for c in customers if c.created_at.month == getCurrentMonth().month
                        and c.created_at.year == getCurrentMonth().year)
        return counted


def getAllCustomerRate():
    with db_session:
        customers = Model.Customer.select()

        last_counted = count(c for c in customers if getLastMonth().month == c.created_at.month
                             and c.created_at.year == getLastMonth().year)
        current_counted = count(c for c in customers if c.created_at.month == getCurrentMonth().month
                                and c.created_at.year == getCurrentMonth().year)
        return (current_counted - last_counted) * 100 / (last_counted if last_counted != 0 else 1)


def getDisbursement():
    with db_session:
        disbursement = Model.Disbursement.select(lambda d: d.dis_date.month == getCurrentMonth().month
                                                 and d.dis_date.year == getCurrentMonth().year)
        return sum(d.balance for d in disbursement)


def getDisbursementRate():
    with db_session:
        disbursement = Model.Disbursement.select()

        last_disbursement = sum(d.balance for d in disbursement if d.dis_date.month == getLastMonth().month
                                and d.dis_date.year == getLastMonth().year)
        current_disbursement = sum(d.balance for d in disbursement if d.dis_date.month == getCurrentMonth().month
                                   and d.dis_date.year == getCurrentMonth().year)
        return (current_disbursement - last_disbursement) * 100 / (last_disbursement if last_disbursement != 0 else 1)


def getCollection():
    with db_session:
        schedule = Model.Schedule.select(lambda s: s.collection_date.month == getCurrentMonth().month
                                                   and s.collection_date.year == getCurrentMonth().year and s.sch_no != 0)
        principal = sum(s.principal for s in schedule if s.principal)
        interest = sum(s.interest for s in schedule if s.interest)
        fee = sum(s.fee for s in schedule if s.fee)
        return principal + interest + fee


def getCollectionRate():
    with db_session:
        last_schedule = Model.Schedule.select(
            lambda s: s.collection_date.month == getLastMonth().month
                      and s.collection_date.year == getLastMonth().year and s.sch_no != 0)
        principal = sum(s.principal for s in last_schedule if s.principal)
        interest = sum(s.interest for s in last_schedule if s.interest)
        fee = sum(s.fee for s in last_schedule if s.fee)
        last_collection = principal + interest + fee

        current_schedule = Model.Schedule.select(
            lambda s: s.collection_date.month == getCurrentMonth().month
                      and s.collection_date.year == getCurrentMonth().year and s.sch_no != 0)
        principal = sum(s.principal for s in current_schedule if s.principal)
        interest = sum(s.interest for s in current_schedule if s.interest)
        fee = sum(s.fee for s in current_schedule if s.fee)
        current_collection = principal + interest + fee

        return round((current_collection - last_collection) * 100 / (last_collection if last_collection != 0 else 1), 2)


def getCollected():
    with db_session:
        try:
            schedule_paid = Model.SchedulePaid.select(
                lambda s: s.paid_date.month == getCurrentMonth().month and s.paid_date.year == getCurrentMonth().year)
            principal = sum(s.principal_paid for s in schedule_paid if s.principal_paid)
            interest = sum(s.interest_paid for s in schedule_paid if s.interest_paid)
            fee = sum(s.fee_paid for s in schedule_paid if s.fee_paid)
        except ValueError:
            pass
        return principal + interest + fee


def getCollectedRate():
    with db_session:
        last_schedule_paid = Model.SchedulePaid.select(lambda s: s.paid_date.month == getLastMonth().month
                                                       and s.paid_date.year == getLastMonth().year)
        principal = sum(s.principal_paid for s in last_schedule_paid if s.principal_paid)
        interest = sum(s.interest_paid for s in last_schedule_paid if s.interest_paid)
        fee = sum(s.fee_paid for s in last_schedule_paid if s.fee_paid)
        last_collected = principal + interest + fee

        current_schedule_paid = Model.SchedulePaid.select(lambda s: s.paid_date.month == getCurrentMonth().month
                                                          and s.paid_date.year == getCurrentMonth().year)
        principal = sum(s.principal_paid for s in current_schedule_paid if s.principal_paid)
        interest = sum(s.interest_paid for s in current_schedule_paid if s.interest_paid)
        fee = sum(s.fee_paid for s in current_schedule_paid if s.fee_paid)
        current_collected = principal + interest + fee

        return round((current_collected - last_collected) * 100 / (last_collected if last_collected != 0 else 1), 2)


def getChartCollection():
    with db_session:
        data = []
        for i in range(1, 13):
            schedule = Model.Schedule.select(lambda s: s.collection_date.month == i
                                                       and s.collection_date.year == getCurrentMonth().year)
            principal = sum(s.principal for s in schedule if s.principal)
            interest = sum(s.interest for s in schedule if s.interest)
            fee = sum(s.fee for s in schedule if s.fee)
            data.append({
                'month': getShortMonth(str(i)),
                'total': principal + interest + fee
            })
        return data


def getChartCollected():
    with db_session:
        data = []
        for i in range(1, 13):
            schedule_paid = Model.SchedulePaid.select(lambda s: s.paid_date.month == i
                                                                     and s.paid_date.year == getCurrentMonth().year)
            principal = sum(s.principal_paid for s in schedule_paid if s.principal_paid)
            interest = sum(s.interest_paid for s in schedule_paid if s.interest_paid)
            fee = sum(s.fee_paid for s in schedule_paid if s.fee_paid)
            data.append({
                'month': getShortMonth(str(i)),
                'total': principal + interest + fee
            })
        return data


def getLastMonth():
    return date.today().replace(day=1) - relativedelta(months=1)


def getNextMonth():
    return date.today().replace(day=1) + relativedelta(months=1)


def getCurrentMonth():
    return date.today().replace(day=1)


def getShortMonth(month: str):
    datetime_object = datetime.datetime.strptime(month, "%m")
    return datetime_object.strftime("%b")


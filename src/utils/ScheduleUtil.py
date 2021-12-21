from ..models.schemasOut import DisbursementOut
from ..models.schemasIn import ScheduleIn
from dateutil import relativedelta, parser
from pony.orm import db_session
from ..models.model import Model
from datetime import datetime


def generateSchedule(disbursement: DisbursementOut) -> bool:
    if disbursement is None:
        return False

    interest = disbursement.balance * disbursement.interest_rate / 100
    fee = disbursement.balance * disbursement.fee_rate / 100

    schedules = {
        0: {
            'sch_no': 0,
            'dis_id': disbursement.id,
            'cus_id': disbursement.cus_id,
            'collection_date': disbursement.dis_date,
            'balance': disbursement.balance,
            'principal': 0,
            'interest': 0,
            'fee': 0,
            'penalty': 0,
            'status': "New"
        },
        1: {
            'collection_date': disbursement.first_date
        }
    }

    for key in range(1, disbursement.duration + 1):

        if key > 1:
            schedules[key] = {}
            schedules[key]['collection_date'] = getNextPay(schedules[key-1]['collection_date'])
        schedules[key]['dis_id'] = disbursement.id
        schedules[key]['cus_id'] = disbursement.cus_id
        schedules[key]['balance'] = disbursement.balance if key != disbursement.duration else 0
        schedules[key]['principal'] = 0 if key != disbursement.duration else disbursement.balance
        schedules[key]['interest'] = interest
        schedules[key]['fee'] = fee
        schedules[key]['penalty'] = 0
        schedules[key]['status'] = 'Not Yet Due'
        schedules[key]['sch_no'] = key

    return storeSchedule(schedules)


def storeSchedule(schedules):
    with db_session:
        for key, value in schedules.items():
            Model.Schedule(**value)
    return True


def getNextPay(old_pay):
    return old_pay + relativedelta.relativedelta(months=1)

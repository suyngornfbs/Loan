from ..models.schemasOut import DisbursementOut
from ..models.schemasIn import ScheduleIn
from dateutil import relativedelta, parser
from pony.orm import db_session
from ..models.model import Model
from datetime import date, datetime
import calendar


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
            schedules[key]['collection_date'] = getNextPay(schedules[key - 1]['collection_date'], disbursement.first_date)
        schedules[key]['dis_id'] = disbursement.id
        schedules[key]['cus_id'] = disbursement.cus_id
        schedules[key]['balance'] = disbursement.balance if key != disbursement.duration else 0
        schedules[key]['principal'] = 0 if key != disbursement.duration else disbursement.balance
        schedules[key]['interest'] = interest
        schedules[key]['fee'] = fee
        schedules[key]['penalty'] = 0
        schedules[key]['status'] = getStatus(schedules[key]['collection_date'])
        schedules[key]['sch_no'] = key

    return storeSchedule(schedules)


def getStatus(cdate):
    if cdate < date.today():
        return "Past Due"
    elif cdate == date.today():
        return "Due Today"
    else:
        return "Not Yet Due"


def storeSchedule(schedules):
    with db_session:
        for key, value in schedules.items():
            Model.Schedule(**value)
    return True


def getNextPay(old_pay, first_pay):
    dt = old_pay + relativedelta.relativedelta(months=1)
    day = first_pay.day
    while True:
        try:
            newdate = dt.replace(day=day)
            break
        except (ValueError, TypeError):
            day -= 1
    return newdate


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def isTheFinalPaid(id: int, sch_no: int):
    with db_session:
        schedules = Model.Schedule.select(lambda s: s.dis_id == id)
        max_sch = max(s.sch_no for s in schedules)
        if max_sch == sch_no:
            return True
        return False


def getPayment(amount, schedule: Model.Schedule):
    global interest_paid, fee_paid
    if amount == 0:
        return [0, 0, 0, 0, 'Amount 0']
    final = []
    paid = []
    status = schedule.status
    if status in ('Past Due', 'Partial Paid But Late'):
        p_status = 'Partial Paid But Late'
        f_status = 'Fully Paid But Late'
    else:
        p_status = 'Partial Paid'
        f_status = 'Fully Paid On Time'
    if amount >= (schedule.interest - cFloat(schedule.interest_paid)):
        final.append(schedule.interest)
        interest_paid = schedule.interest - cFloat(schedule.interest_paid)
        paid.append(interest_paid)
        if (schedule.interest - cFloat(schedule.interest_paid)) > 0:
            amount = amount - (schedule.interest - cFloat(schedule.interest_paid))
    elif amount < (schedule.interest - cFloat(schedule.interest_paid)):
        return [amount + cFloat(schedule.interest_paid), 0, 0, 0, p_status, amount, 0, 0]

    if amount >= (schedule.fee - cFloat(schedule.fee_paid)):
        final.append(schedule.fee)
        fee_paid = schedule.fee - cFloat(schedule.fee_paid)
        paid.append(fee_paid)
        if (schedule.fee - cFloat(schedule.fee_paid)) > 0:
            amount = amount - (schedule.fee - cFloat(schedule.fee_paid))
    else:
        x = schedule.fee - cFloat(schedule.fee_paid)
        return [schedule.interest, amount + cFloat(schedule.fee_paid), interest_paid, 0, p_status, interest_paid,
                amount, 0]

    if amount >= (schedule.principal - cFloat(schedule.principal_paid)):
        final.append(schedule.principal)
        paid.append(schedule.principal - cFloat(schedule.principal_paid))
        amount = amount - (schedule.principal - cFloat(schedule.principal_paid))
        final.append(amount)
        final.append(f_status)
        return [*final, *paid]
    else:
        return [schedule.interest, schedule.fee, amount + cFloat(schedule.principal_paid), 0, p_status, interest_paid,
                fee_paid, amount]


def updatePay(schedules: Model.Schedule, pay):
    with db_session:
        try:
            schedules.status = pay[4]
            schedules.principal_paid = pay[2]
            schedules.interest_paid = pay[0]
            schedules.fee_paid = pay[1]
            schedules.penalty_paid = 0
            schedules.collected_date = date.today()
            if isTheFinalPaid(schedules.dis_id, schedules.sch_no) and pay[4] in (
                    'Fully Paid On Time', 'Fully Paid But Late'):
                Model.Disbursement[schedules.dis_id].status = "Closed"
            Model.SchedulePaid(
                dis_id=schedules.dis_id,
                sch_id=schedules.id,
                invoice=invoice(),
                paid_date=date.today(),
                payment_date=schedules.collection_date,
                interest_paid=pay[5],
                penalty_paid=0,
                fee_paid=pay[6],
                principal_paid=pay[7],
                status='Close',
            )
            return True
        except ValueError:
            return False


def invoice():
    with db_session:
        schedule = Model.Schedule.select()
        count = max(s.id for s in schedule)
        # count = False
        if not count:
            return 'paid_0000'
        return 'paid_' + str(count)


def cFloat(num):
    if num is None:
        return 0
    return num

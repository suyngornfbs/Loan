from pony.orm import *
from ..models.model import Model
from datetime import date


def getDisbursedCode():
    with db_session:
        counted = max(c.id for c in Model.Disbursement)
        if counted is None:
            counted = 0
        while True:
            code = "loan_" + str(counted + 1)
            cus_code = Model.Customer.get(lambda c: c.cus_code == code)
            if cus_code is not None:
                counted += 1
                continue
            break
        return code


def checkValidation(request):
    message = []
    check = True
    if not request.cus_id or request.cus_id == 0:
        message.append('cus_id cannot 0')
        check = False
    elif not isCustomer(request.cus_id):
        message.append(f'Customer id:{request.cus_id}  not found')
        check = False

    if not request.repayment_method or request.repayment_method != "Balloon":
        message.append('repayment_method is request! or must be balloon')
        check = False

    if request.interest_rate is None:
        message.append('interest_rate is request')
        check = False

    elif not isinstance(request.interest_rate, float):
        message.append('interest_rate request float')
        check = False

    if not request.dis_date:
        message.append('Disbursement Date is request!')
        check = False
    elif not request.first_date:
        message.append('First payment date is request!')
        check = False
    elif request.dis_date >= request.first_date:
        message.append('First payment date must be bigger than disbursement date!')
        check = False

    return [check, {'message': message}]


def isCustomer(id) -> bool:
    with db_session:
        customer = Model.Customer.get(lambda c: c.id == id)
        if customer is None:
            return False
        return True


def paynow(disbursement_id: int):
    with db_session:
        close = Model.Disbursement.get(lambda d: d.id == disbursement_id)
        if close.status == 'Closed':
            return {
                'disbursement': 'Closed'
            }
        schedule = Model.Schedule.select(lambda s: s.dis_id == disbursement_id and s.status in (
            'Not Yet Due', 'Partial Paid', 'Past Due', 'Due Today', 'Partial Paid But Late'))
        allPay = getAllTotalPay(schedule)
        schedule_dict = {
            'principal': allPay[0],
            'interest': allPay[1],
            'fee': allPay[2],
            'penalty': 0,
            'total': allPay[3],
            'date': date.today()
        }

        return schedule_dict


def getAllTotalPay(schedules):
    if schedules.first().status in ('Due Today', 'Not Yet Due', 'Partial Paid'):
        schedule = schedules.first()
        principal = schedule.principal - cFloat(schedule.principal_paid)
        interest = schedule.interest - cFloat(schedule.interest_paid)
        fee = schedule.fee - cFloat(schedule.fee_paid)
        total = totalPaynow(schedule)
        return [principal, interest, fee, total]

    principal = interest = fee = total = 0
    for schedule in schedules:
        if schedule.status == "Not Yet Due":
            break
        principal += schedule.principal - cFloat(schedule.principal_paid)
        interest += schedule.interest - cFloat(schedule.interest_paid)
        fee += schedule.fee - cFloat(schedule.fee_paid)
        total += totalPaynow(schedule)
    return [principal, interest, fee, total]


def totalPaynow(schedule: Model.Schedule):
    total = schedule.fee + schedule.principal + schedule.interest - \
            cFloat(schedule.interest_paid) - cFloat(schedule.principal_paid) - cFloat(schedule.fee_paid)
    return total


def totalPayment(schedule: Model.Schedule, amount) -> int:
    with db_session:
        total = cFloat(schedule.principal) + cFloat(schedule.fee) + cFloat(schedule.interest) + \
                cFloat(schedule.penalty) - cFloat(schedule.principal_paid) - cFloat(schedule.interest_paid) - \
                cFloat(schedule.fee_paid) - cFloat(schedule.penalty_paid)
        if total == amount:
            return 1
        elif total > amount:
            return 2
        else:
            return 3


def cFloat(num):
    if num is None:
        return 0
    return num


def payOff(id: int):
    with db_session:
        schedules = Model.Schedule.select(
            lambda s: s.dis_id == id and s.status in ('Not Yet Due', 'Partial Paid', 'Past Due', 'Due Today',
                                                      'Partial Paid But Late')).first()
        if not schedules:
            return {
                'message': "something went wrong!"
            }
        collection_date = schedules.collection_date
        date_count = date.today() - collection_date
        if date_count > 0:
            return date_count

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
    if request.cus_id == 0:
        message.append('cus_id cannot 0')
        check = False
    elif not isCustomer(request.cus_id):
        message.append(f'Customer id:{request.cus_id}  not found')
        check = False

    if request.repayment_method is None or request.repayment_method == "":
        message.append('repayment_method is request!')
        check = False

    if request.interest_rate is None:
        message.append('interest_rate is request')
        check = False

    elif not isinstance(request.interest_rate, float):
        message.append('interest_rate request float')
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
        schedule = Model.Schedule.select(lambda s: s.dis_id == disbursement_id and s.status == "Not Yet Due").first()
        schedule_dict = {
            'principal': schedule.principal,
            'interest': schedule.interest,
            'fee': schedule.fee,
            'penalty': schedule.penalty,
            'total': totalPaynow(schedule),
            'date': date.today()
        }

        return schedule_dict


def totalPaynow(schedule: Model.Schedule):
    total = schedule.fee + schedule.principal + schedule.interest + schedule.penalty
    return total


def totalPayment(schedule: Model.Schedule, amount) -> bool:
    with db_session:
        total = cFloat(schedule.principal) + cFloat(schedule.fee) + cFloat(schedule.interest) + \
                cFloat(schedule.penalty) - cFloat(schedule.principal_paid) - cFloat(schedule.interest_paid) - \
                cFloat(schedule.fee_paid) - cFloat(schedule.penalty_paid)
        if total == amount:
            return True
        return False


def cFloat(num):
    if num is None:
        return 0
    return num

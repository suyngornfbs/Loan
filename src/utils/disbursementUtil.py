from pony.orm import *
from ..models.model import Model


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

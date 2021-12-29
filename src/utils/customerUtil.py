from pony.orm import *
from ..models.model import Model


def getCusCode() -> str:
    with db_session:
        counted = max(c.id for c in Model.Customer)
        if counted is None:
            counted = 0
        while True:
            code = "cus_" + str(counted + 1)
            cus_code = Model.Customer.get(lambda c: c.cus_code == code)
            if cus_code is not None:
                counted += 1
                continue
            break
        return code


def validation(request):
    message = []
    check = True
    if request.first_name is None or request.first_name == '':
        message.append('first name is request')
        check = False
    if request.last_name is None or request.first_name == '':
        message.append('last name is request!')
        check = False

    return [check, {
        'success': 0,
        'message': message
    }]



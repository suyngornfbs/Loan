from pony.orm import *
from ..models.model import Model


def getCusCode() -> str:
    with db_session:
        counted = max(c.id for c in Model.Customer)
        while True:
            code = "cus_" + str(counted + 1)
            cus_code = Model.Customer.get(lambda c: c.cus_code == code)
            if cus_code is not None:
                counted += 1
                continue
            break
        return code

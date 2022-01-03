from ..models.model import Model
from pony.orm import *


def disbursementResource(disbursement: Model.Disbursement):
    with db_session:
        return {
            'dis_id': disbursement.id,
            'dis_code': disbursement.dis_code,
            'cus_id': disbursement.cus_id,
            'cus_firstname': Model.Customer.get(id=disbursement.cus_id).first_name,
            'cus_lastname': Model.Customer.get(id=disbursement.cus_id).last_name,
            'status': disbursement.status,
            'product_type': disbursement.product_type,
            'repayment_method': disbursement.repayment_method,
            'interest_rate': disbursement.interest_rate,
            'fee_rate': disbursement.fee_rate,
            'balance': disbursement.balance,
            'dis_date': disbursement.dis_date,
            'first_date': disbursement.first_date,
            'duration': disbursement.duration,
            'frequency': disbursement.frequency
        }

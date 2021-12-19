from fastapi import APIRouter, Request, status
from pony.orm import db_session
from fastapi import Depends
from ..config.auth import get_current_user
from ..models.schemasIn import UserIn, DisbursementIn
from ..models.schemasOut import DisbursementOut
from ..models.model import Model

router = APIRouter()


@router.get('/disbursement', tags=['Disbursement'])
def all(current_user: UserIn = Depends(get_current_user)):
    with db_session:
        disbursement = Model.Disbursement.select()
        return [DisbursementOut.from_orm(d) for d in disbursement]

@router.get('/disbursement/{id}', tags=['Disbursement'])
def get(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        disbursement = Model.Disbursement.get(lambda d: d.id == id)
        if not disbursement:
            return {'message': f'Disbursement Id:{id} not found'}
        return DisbursementOut.from_orm(disbursement)


@router.post('/disbursement', tags=['Disbursement'])
def create(request: DisbursementIn, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        try:
            disbursement = Model.Disbursement(
                dis_code="Loan_001",
                cus_id=request.cus_id if request.cus_id is not None else 0,
                gran_id=request.gran_id if request.gran_id is not None else 0,
                col_id=request.col_id if request.col_id is not None else 0,
                branch_id=request.branch_id if request.branch_id is not None else 0,
                status=request.status if request.status is not None else "",
                product_type=request.product_type if request.product_type is not None else "",
                repayment_method=request.repayment_method if request.repayment_method is not None else "",
                interest_rate=request.interest_rate if request.interest_rate is not None else 0,
                balance=request.balance if request.balance is not None else 0,
                term=request.term if request.term is not None else 0,
                step=request.step if request.step is not None else 0,
                duration=request.duration if request.duration is not None else 0,
                interest_term=request.interest_term if request.interest_term is not None else "",
                propose_amount=request.propose_amount if request.propose_amount is not None else 0,
                approve_amount=request.approve_amount if request.approve_amount is not None else 0,
                principal=request.principal if request.principal is not None else 0,
                fee_rate=request.fee_rate if request.fee_rate is not None else 0,
                dis_date=request.dis_date if request.dis_date is not None else "",
                first_date=request.first_date if request.first_date is not None else "",
                purpose=request.purpose if request.purpose is not None else "",
                day_in_month=request.day_in_month if request.day_in_month is not None else 0,
                day_in_year=request.day_in_year if request.day_in_year is not None else 0,
                holiday_weekend=request.holiday_weekend if request.holiday_weekend is not None else "",
                contract_by=request.contract_by if request.contract_by is not None else 0,
                created_by=request.created_by if request.created_by is not None else 0,
                updated_by=request.updated_by if request.updated_by is not None else 0,
                created_at=request.created_at if request.created_at is not None else "",
                updated_at=request.created_at if request.created_at is not None else "",
                deleted_at=request.deleted_at if request.deleted_at is not None else "",
            )
            return DisbursementOut.from_orm(disbursement)
        except RuntimeError:
            return {'message': "Error"}


@router.put('/disbursement/{id}', tags=['Disbursement'])
def update(id: int, request: DisbursementIn, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        disbursement = Model.Disbursement.get(lambda d: d.id == id)
        if not disbursement:
            return {'message': f'Disbursement Id:{id} not found'}
        disbursement.dis_code = "Loan_001"
        disbursement.cus_id = request.cus_id if request is not None else 0
        disbursement.gran_id = request.gran_id if request.gran_id is not None else 0
        disbursement.col_id = request.col_id if request.col_id is not None else 0
        disbursement.branch_id = request.branch_id if request.branch_id is not None else 0
        disbursement.status = request.status if request.status is not None else ""
        disbursement.product_type = request.product_type if request.product_type is not None else ""
        disbursement.repayment_method = request.repayment_method if request.repayment_method is not None else ""
        disbursement.interest_rate = request.interest_rate if request.interest_rate is not None else 0
        disbursement.balance = request.balance if request.balance is not None else 0
        disbursement.term = request.term if request.term is not None else 0
        disbursement.step = request.step if request.step is not None else 0
        disbursement.duration = request.duration if request.duration is not None else 0
        disbursement.interest_term = request.interest_term if request.interest_term is not None else ""
        disbursement.propose_amount = request.propose_amount if request.propose_amount is not None else 0
        disbursement.approve_amount = request.approve_amount if request.approve_amount is not None else 0
        disbursement.principal = request.principal if request.principal is not None else 0
        disbursement.fee_rate = request.fee_rate if request.fee_rate is not None else 0
        disbursement.dis_date = request.dis_date if request.dis_date is not None else ""
        disbursement.first_date = request.first_date if request.first_date is not None else ""
        disbursement.purpose = request.purpose if request.purpose is not None else ""
        disbursement.day_in_month = request.day_in_month if request.day_in_month is not None else 0
        disbursement.day_in_year = request.day_in_year if request.day_in_year is not None else 0
        disbursement.holiday_weekend = request.holiday_weekend if request.holiday_weekend is not None else ""
        disbursement.contract_by = request.contract_by if request.contract_by is not None else 0
        disbursement.created_by = request.created_by if request.created_by is not None else 0
        disbursement.updated_by = request.updated_by if request.updated_by is not None else 0
        disbursement.created_at = request.created_at if request.created_at is not None else ""
        disbursement.updated_at = request.updated_at if request.updated_at is not None else ""
        disbursement.deleted_at = request.deleted_at if request.deleted_at is not None else ""
        return DisbursementOut.from_orm(disbursement)


@router.delete('/disbursement/{id}', tags=['Disbursement'])
def delete(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        disbursement = Model.Disbursement.select(lambda d: d.id == id)
        if disbursement:
            disbursement.delete()
            return {
                'message': 'Delete successfully'
            }
        return {'message': f'Disbursement Id:{id} not found'}

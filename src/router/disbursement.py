from fastapi import APIRouter, Request, status
from pony.orm import db_session
from fastapi import Depends
from ..config.auth import get_current_user
from ..models.schemasIn import UserIn, DisbursementIn
from ..models.schemasOut import DisbursementOut
from ..models.model import Model
from ..utils.disbursementUtil import *
from datetime import date

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
            check, validation = checkValidation(request)
            if not check:
                return validation

            disbursement = Model.Disbursement(
                dis_code=getDisbursedCode(),
                cus_id=request.cus_id if request.cus_id is not None else 0,
                status="New",
                repayment_method=request.repayment_method if request.repayment_method is not None else "",
                interest_rate=request.interest_rate if request.interest_rate is not None else 0,
                balance=request.balance if request.balance is not None else 0,
                step=request.step if request.step is not None else 0,
                duration=request.duration if request.duration is not None else 0,
                fee_rate=request.fee_rate if request.fee_rate is not None else 0,
                dis_date=request.dis_date if request.dis_date is not None else "",
                first_date=request.first_date if request.first_date is not None else "",
                created_at=request.created_at if request.created_at is not None else date.today(),
                updated_at=request.created_at if request.created_at is not None else date.today(),
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
        disbursement.cus_id = request.cus_id if request is not None else 0
        disbursement.repayment_method = request.repayment_method if request.repayment_method is not None else ""
        disbursement.interest_rate = request.interest_rate if request.interest_rate is not None else 0
        disbursement.balance = request.balance if request.balance is not None else 0
        disbursement.step = request.step if request.step is not None else 0
        disbursement.duration = request.duration if request.duration is not None else 0
        disbursement.fee_rate = request.fee_rate if request.fee_rate is not None else 0
        disbursement.dis_date = request.dis_date if request.dis_date is not None else ""
        disbursement.first_date = request.first_date if request.first_date is not None else ""
        disbursement.updated_at = request.updated_at if request.updated_at is not None else date.today()

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

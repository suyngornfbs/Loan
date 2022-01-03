from fastapi import APIRouter, Request, status, Depends
from pony.orm import db_session
from ..config.auth import get_current_user
from ..models.schemasIn import UserIn, DisbursementIn
from ..models.schemasOut import DisbursementOut
from ..models.model import Model
from ..utils.disbursementUtil import *
from ..utils.ScheduleUtil import generateSchedule
from datetime import date
from ..config.auth import get_current_user
from ..resource import resource

router = APIRouter()


@router.get('/disbursement', tags=['Disbursement'])
def all(current_user: UserIn = Depends(get_current_user)):
    with db_session:
        disbursement = Model.Disbursement.select()
        if not disbursement:
            return {
                'success': 1,
                'message': 'Disbursement is empty!'
            }
        return {
            'success': 1,
            'data': [resource.disbursementResource(d) for d in disbursement]
        }


@router.get('/disbursement/{id}', tags=['Disbursement'])
def get(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        disbursement = Model.Disbursement.get(lambda d: d.id == id)
        if not disbursement:
            return {
                'success': 0,
                'message': f'Disbursement Id:{id} not found'}
        return {
            'success': 1,
            'data': resource.disbursementResource(disbursement)
        }


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
                status="Approved",
                repayment_method=request.repayment_method if request.repayment_method is not None else "",
                interest_rate=request.interest_rate if request.interest_rate is not None else 0,
                balance=request.balance if request.balance is not None else 0,
                frequency=request.frequency if request.frequency is not None else 0,
                duration=request.duration if request.duration is not None else 0,
                fee_rate=request.fee_rate if request.fee_rate is not None else 0,
                dis_date=request.dis_date if request.dis_date is not None else "",
                first_date=request.first_date if request.first_date is not None else "",
                product_type=request.product_type if request.product_type else "",
                created_at=request.created_at if request.created_at is not None else date.today(),
                updated_at=request.created_at if request.created_at is not None else date.today(),
                interest_period=request.interest_period if request.interest_period else "",
                duration_period=request.duration_period if request.duration_period else ""
            )
            Model.Customer[request.cus_id].status = "Active"
            dis = Model.Disbursement.get(lambda d: d.dis_code == disbursement.dis_code)
            generateSchedule(DisbursementOut.from_orm(dis))
            return {
                'success': 1,
                'data': "Create disbursement successful"
            }
        except RuntimeError:
            return {
                'success': 0,
                'message': "Error"
            }


# @router.put('/disbursement/{id}', tags=['Disbursement'])
def update(id: int, request: DisbursementIn, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        disbursement = Model.Disbursement.get(lambda d: d.id == id)
        if not disbursement:
            return {
                'success': 0,
                'message': f'Disbursement Id:{id} not found'
            }
        disbursement.cus_id = request.cus_id if request is not None else 0
        disbursement.repayment_method = request.repayment_method if request.repayment_method is not None else ""
        disbursement.interest_rate = request.interest_rate if request.interest_rate is not None else 0
        disbursement.balance = request.balance if request.balance is not None else 0
        disbursement.frequency = request.frequency if request.frequency is not None else 0
        disbursement.duration = request.duration if request.duration is not None else 0
        disbursement.fee_rate = request.fee_rate if request.fee_rate is not None else 0
        disbursement.dis_date = request.dis_date if request.dis_date is not None else ""
        disbursement.first_date = request.first_date if request.first_date is not None else ""
        disbursement.updated_at = request.updated_at if request.updated_at is not None else date.today()
        disbursement.interest_period = request.interest_period if request.interest_period else ""
        disbursement.duration_period = request.duration_period if request.duration_period else ""

        return {
            'success': 1,
            'data': "Update disbursement successful"
        }


# @router.delete('/disbursement/{id}', tags=['Disbursement'])
def delete(id: int):
    with db_session:
        disbursement = Model.Disbursement.select(lambda d: d.id == id)
        if disbursement:
            disbursement.delete()
            return {
                'success': 1,
                'message': 'Delete successfully'
            }
        return {
            'success': 0,
            'message': f'Disbursement Id:{id} not found'}

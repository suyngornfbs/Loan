from datetime import datetime

from fastapi import APIRouter, Request, status
from pony.orm import db_session
from fastapi import Depends
from ..config.auth import get_current_user
from ..models.schemasIn import CustomerIn, UserIn
from ..models.schemasOut import CustomerOut
from ..models.model import Model

router = APIRouter()


@router.post('/customer', tags=['Customers'])
def create_customer(request: CustomerIn, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        try:
            customer = Model.Customer(
                cus_code="CUS_2022",
                first_name=request.first_name if request.first_name is not None else "",
                last_name=request.last_name if request.last_name is not None else "",
                gender=request.gender if request.gender is not None else "",
                dob=request.dob if request is not None else "",
                phone=request.phone if request.dob is not None else "",
                nationality=request.nationality if request.nationality is not None else "",
                email=request.email if request.email is not None else "",
                identity_type=request.identity_type if request.identity_type is not None else "",
                identity_number=request.identity_number if request.identity_number is not None else "",
                identity_date=request.identity_date if request.identity_date is not None else "",
                id_card=request.id_card if request.id_card is not None else "",
                street_no=request.street_no if request.street_no is not None else "",
                address=request.address if request.address is not None else "",
                status=request.status if request.status is not None else "",
                profile_img=request.profile_img if request.profile_img is not None else "",
                attachment_file=request.attachment_file if request.attachment_file is not None else "",
                occupation=request.occupation if request.occupation is not None else "",
                income=request.income if request.income is not None else "",
                updated_by=request.updated_by if request.updated_by is not None else "",
                created_by=request.created_by if request.created_by is not None else "",
                created_at=request.crated_at if request.crated_at is not None else "",
                updated_at=request.crated_at if request.crated_at is not None else "",
            )
        except RuntimeError:
            pass

        return CustomerIn.from_orm(customer)


@router.get('/customer', tags=['Customers'])
def get_all_customer(current_user: UserIn = Depends(get_current_user)):
    with db_session:
        customer = Model.Customer.select()
        return [CustomerOut.from_orm(c) for c in customer]


@router.get('/customer/{id}', tags=['Customers'])
def get_customer_by_id(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        customer = CustomerOut.from_orm(Model.Customer[id])
        if not customer:
            return {
                'message': f'Customer Id:{id} not found'
            }
        return customer


@router.put('/customer/{id}', tags=['Customers'])
def update_customer(id: int, request: CustomerIn, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        customer = Model.Customer.get(lambda c: c.id == id)
        if not customer:
            return {
                 'message': f'Customer Id:{id} not found'
            }
        customer.first_name = request.first_name if request.first_name is not None else ""
        customer.last_name = request.last_name if request.last_name is not None else ""
        customer.gender = request.gender if request.gender is not None else ""
        customer.dob = request.dob if request is not None else ""
        customer.phone = request.phone if request.dob is not None else ""
        customer.nationality = request.nationality if request.nationality is not None else ""
        customer.email = request.email if request.email is not None else ""
        customer.identity_type = request.identity_type if request.identity_type is not None else ""
        customer.identity_number = request.identity_number if request.identity_number is not None else ""
        customer.identity_date = request.identity_date if request.identity_date is not None else ""
        customer.id_card = request.id_card if request.id_card is not None else ""
        customer.street_no = request.street_no if request.street_no is not None else ""
        customer.address = request.address if request.address is not None else ""
        customer.status = request.status if request.status is not None else ""
        customer.profile_img = request.profile_img if request.profile_img is not None else ""
        customer.attachment_file = request.attachment_file if request.attachment_file is not None else ""
        customer.occupation = request.occupation if request.occupation is not None else ""
        customer.income = request.income if request.income is not None else ""
        customer.updated_by = request.updated_by if request.updated_by is not None else ""
        customer.created_by = request.created_by if request.created_by is not None else ""
        customer.created_at = request.crated_at if request.crated_at is not None else ""
        customer.updated_at = request.crated_at if request.crated_at is not None else ""
        return CustomerOut.from_orm(customer)


@router.delete('/customer/{id}', tags=['Customers'])
def delete_customer(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        customer = Model.Customer.select(lambda c: c.id == id)
        if customer:
            customer.delete()
            return {
                'message': 'Delete successfully'
            }
        return {
            'message': f'Customer Id:{id} not found'
        }

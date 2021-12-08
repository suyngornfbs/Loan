from fastapi import APIRouter
from pony.orm import db_session
from ..models.schemas import CustomerToDB
from ..models.model import Model

router = APIRouter()


# @router.post('/customer', tags=['Customers'])
# def create_customer(request: CustomerToDB):
#     with db_session:
#         Model.Customer(
#             cus_code="09876",
#             first_name=request.first_name,
#             last_name=request.last_name
#         )
#         return {"message": "Create Successfully!!"}
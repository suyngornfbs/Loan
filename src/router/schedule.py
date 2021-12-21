from fastapi import APIRouter, Depends
from ..models.schemasIn import UserIn
from ..models.schemasOut import ScheduleOut
from ..models.model import Model
from ..config.auth import get_current_user
from pony.orm import db_session

router = APIRouter()


@router.get('/disbursement/{id}/schedule', tags=['Schedule'])
def scheduleByLoan(id: int, current_user: UserIn = Depends(get_current_user)):
    with db_session:
        schedules = Model.Schedule.select(lambda s: s.dis_id == id)
        if schedules is not None:
            return [ScheduleOut.from_orm(s) for s in schedules]
        return {
            'message': 'disbursement or schedule not defined!'
        }

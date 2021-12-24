from ..models.model import Model
from ..models.schemasOut import ScheduleOut
from pony.orm import db_session


class Payment:
    def __init__(self, disbursement, request):
        self.request = request
        self.disbursement = disbursement

    def getSchedule(self):
        with db_session:

            return Model.Schedule.get(lambda s: s.dis_id == self.disbursement)

    def pay(self):
        with db_session:
            schedules = self.getSchedule()
            sch = [ScheduleOut.from_orm(s) for s in schedules]
            return sch

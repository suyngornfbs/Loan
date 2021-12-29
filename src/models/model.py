from pony.orm import *
from datetime import date
from ..config.settings import Setting


class Model:
    db = Database()
    db.bind(**Setting.get_bind(db))

    def __init__(self):
        pass

    class User(db.Entity):
        _table_ = 'users'
        id = PrimaryKey(int, auto=True)
        name = Optional(str, 255)
        email = Optional(str, 255, unique=True)
        password = Optional(str, 255)
        dob = Optional(date)
        gender = Optional(str, 255)
        expires_in = Optional(str, 255)
        profile_img = Optional(str, 255)
        about_me = Optional(str, 255)
        address = Optional(str, 255)

    class Role(db.Entity):
        _table_ = 'roles'
        id = PrimaryKey(int, auto=True)
        name = Optional(str, 255, unique=True)

    class Permission(db.Entity):
        _table_ = 'permissions'
        id = PrimaryKey(int, auto=True)
        name = Optional(str, 255, unique=True)

    class UserHasRole(db.Entity):
        _table_ = "user_has_role"
        user_id = Optional(int)
        role_id = Optional(int)

    class RoleHasPermission(db.Entity):
        _table_ = "role_has_permission"
        role_id = Optional(int)
        permission_id = Optional(int)

    class Customer(db.Entity):
        _table_ = "customers"
        id = PrimaryKey(int, auto=True)
        cus_code = Optional(str, 255)
        first_name = Optional(str)
        last_name = Optional(str)
        gender = Optional(str, 10)
        dob = Optional(date)
        phone = Optional(str, 20)
        nationality = Optional(str)
        email = Optional(str)
        identity_type = Optional(str)
        identity_number = Optional(str)
        identity_date = Optional(str)
        id_card = Optional(str)
        house_no = Optional(str)
        street_no = Optional(str)
        address = Optional(str)
        status = Optional(str)
        profile_img = Optional(str)
        attachment_file = Optional(str)
        occupation = Optional(str)
        income = Optional(float)
        created_by = Optional(int)
        updated_by = Optional(int)
        created_at = Optional(date)
        updated_at = Optional(date)
        deleted_at = Optional(date)

    class Disbursement(db.Entity):
        _table_ = "disbursements"
        id = PrimaryKey(int, auto=True)
        dis_code = Optional(str)
        cus_id = Optional(int)
        gran_id = Optional(int)
        col_id = Optional(int)
        branch_id = Optional(int)
        status = Optional(str)
        product_type = Optional(str)
        repayment_method = Optional(str)
        interest_rate = Optional(float)
        balance = Optional(float)
        term = Optional(int)
        step = Optional(int)
        duration = Optional(int)
        interest_term = Optional(int)
        propose_amount = Optional(float)
        approve_amount = Optional(float)
        principal = Optional(float)
        fee_rate = Optional(float)
        dis_date = Optional(date)
        first_date = Optional(date)
        purpose = Optional(str)
        day_in_month = Optional(int)
        day_in_year = Optional(int)
        holiday_weekend = Optional(str)
        contract_by = Optional(int)
        created_by = Optional(int)
        updated_by = Optional(int)
        created_at = Optional(date)
        updated_at = Optional(date)
        deleted_at = Optional(date)

    class Schedule(db.Entity):
        _table_ = "schedules"
        id = PrimaryKey(int, auto=True)
        cus_id = Optional(int)
        dis_id = Optional(int)
        collection_date = Optional(date)
        collected_date = Optional(date)
        status = Optional(str)
        sch_no = Optional(int)
        count_late_day = Optional(int)
        balance = Optional(float)
        principal = Optional(float)
        principal_paid = Optional(float)
        interest = Optional(float)
        interest_paid = Optional(float)
        fee = Optional(float)
        fee_paid = Optional(float)
        penalty = Optional(float)
        penalty_paid = Optional(float)
        received_by = Optional(int)
        is_renew = Optional(str)
        is_reschedule = Optional(str)
        is_restructure = Optional(str)
        is_amendment = Optional(str)
        created_by = Optional(int)
        updated_by = Optional(int)
        created_at = Optional(date)
        updated_at = Optional(date)
        deleted_at = Optional(date)

    class SchedulePaid(db.Entity):
        _table_ = "schedule_paid"
        id = PrimaryKey(int, auto=True)
        sch_id = Optional(int)
        invoice = Optional(str)
        paid_date = Optional(date)
        payment_date = Optional(date)
        interest_paid = Optional(float)
        fee_paid = Optional(float)
        principal_paid = Optional(float)
        penalty_paid = Optional(float)
        paid_total = Optional(float)
        paid_off_note = Optional(str)
        status = Optional(str)
        created_by = Optional(int)
        created_at = Optional(date)
        updated_by = Optional(int)
        updated_at = Optional(date)

    db.generate_mapping(create_tables=True)



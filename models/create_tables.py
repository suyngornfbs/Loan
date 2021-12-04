from datetime import date


def migration(db, orm):
    class User(db.Entity):
        __table__ = 'users'
        id = orm.PrimaryKey(int, auto=True)
        name = orm.Required(str, 255)
        email = orm.Required(str, 255, unique=True)
        password = orm.Required(str, 255)
        user_has__roles = orm.Set('User_has_Role')

    class Role(db.Entity):
        __table_ = 'roles'
        id = orm.PrimaryKey(int, auto=True)
        name = orm.Required(str, 255, unique=True)
        user_has__roles = orm.Set('User_has_Role')
        role_has_permissions = orm.Set('Role_has_permission')

    class Permission(db.Entity):
        __table__ = 'permissions'
        id = orm.PrimaryKey(int, auto=True)
        name = orm.Required(str, 255, unique=True)
        role_has_permissions = orm.Set('Role_has_permission')

    class User_has_Role(db.Entity):
        __table__ = "user_has_role"
        users = orm.Optional(User)
        roles = orm.Optional(Role)

    class Role_has_permission(db.Entity):
        __table__ = "role_has_permission"
        roles = orm.Optional(Role)
        permissions = orm.Optional(Permission)

    class Customer(db.Entity):
        __table__ = "customers"
        id = orm.PrimaryKey(int, auto=True)
        cus_code = orm.Required(str, 255)
        first_name = orm.Required(str)
        last_name = orm.Required(str)
        gender = orm.Required(str, 10)
        dob = orm.Optional(date)
        phone = orm.Required(str, 20)
        nationality = orm.Optional(str)
        email = orm.Optional(str)
        identity_type = orm.Optional(str)
        identity_number = orm.Optional(str)
        identity_date = orm.Optional(str)
        id_card = orm.Optional(str)
        house_no = orm.Optional(str)
        street_no = orm.Optional(str)
        address = orm.Optional(str)
        status = orm.Required(str)
        profile_img = orm.Optional(str)
        attachment_file = orm.Optional(str)
        occupation = orm.Optional(str)
        income = orm.Optional(int)
        created_by = orm.Optional(int)
        updated_by = orm.Optional(int)
        created_at = orm.Optional(date)
        updated_at = orm.Optional(date)
        deleted_at = orm.Optional(date)

    class Disbursement(db.Entity):
        __table__ = "disbursements"
        id = orm.PrimaryKey(int, auto=True)
        dis_code = orm.Optional(str)
        cus_id = orm.Required(int)
        gran_id = orm.Optional(int)
        col_id = orm.Optional(int)
        branch_id = orm.Optional(int)
        status = orm.Required(str)
        product_type = orm.Optional(str)
        repayment_method = orm.Required(str)
        interest_rate = orm.Required(float)
        balance = orm.Optional(float)
        term = orm.Optional(int)
        step = orm.Required(int)
        duration = orm.Required(int)
        interest_term = orm.Optional(int)
        propose_amount = orm.Required(float)
        approve_amount = orm.Optional(float)
        principal = orm.Optional(float)
        fee_rate = orm.Required(float)
        dis_date = orm.Required(date)
        first_date = orm.Optional(date)
        purpose = orm.Optional(str)
        day_in_month = orm.Optional(int)
        day_in_year = orm.Optional(int)
        holiday_weekend = orm.Optional(str)
        contract_by = orm.Optional(int)
        created_by = orm.Optional(int)
        updated_by = orm.Optional(int)
        created_at = orm.Optional(date)
        updated_at = orm.Optional(date)
        deleted_at = orm.Optional(date)

    class Schedule(db.Entity):
        __table__ = "schedules"
        id = orm.PrimaryKey(int, auto=True)
        cus_id = orm.Required(int)
        dis_id = orm.Required(int)
        collection_date = orm.Optional(date)
        collected_date = orm.Optional(date)
        status = orm.Optional(str)
        sch_no = orm.Optional(int)
        count_late_day = orm.Optional(int)
        balance = orm.Optional(float)
        principal = orm.Optional(float)
        principal_paid = orm.Optional(float)
        interest = orm.Optional(float)
        interest_paid = orm.Optional(float)
        fee = orm.Optional(float)
        fee_paid = orm.Optional(float)
        penalty = orm.Optional(float)
        penalty_paid = orm.Optional(float)
        received_by = orm.Optional(int)
        is_renew = orm.Optional(str)
        is_reschedule = orm.Optional(str)
        is_restructure = orm.Optional(str)
        is_amendment = orm.Optional(str)
        created_by = orm.Optional(int)
        updated_by = orm.Optional(int)
        created_at = orm.Optional(date)
        updated_at = orm.Optional(date)
        deleted_at = orm.Optional(date)

    class Schedule_paid(db.Entity):
        __table__ = "schedules"
        id = orm.PrimaryKey(int, auto=True)
        sch_id = orm.Required(int)
        invoice = orm.Optional(str)
        paid_date = orm.Optional(str)
        payment_date = orm.Optional(date)
        interest_paid = orm.Optional(float)
        fee_paid = orm.Optional(float)
        principal_paid = orm.Optional(float)
        penalty_paid = orm.Optional(float)
        paid_total = orm.Optional(float)
        paid_off_note = orm.Optional(str)
        status = orm.Optional(str)
        created_by = orm.Optional(int)
        created_at = orm.Optional(date)
        updated_by = orm.Optional(int)
        updated_at = orm.Optional(date)
        deleted_at = orm.Optional(date)

    return [
        User,
        Role,
        Permission,
        User_has_Role,
        Role_has_permission,
        Customer,
        Disbursement,
        Schedule,
        Schedule_paid
    ]

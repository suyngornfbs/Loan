from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:

    def __init__(self):
        pass

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self)

    def get_password_hash(self):
        return pwd_context.hash(self)

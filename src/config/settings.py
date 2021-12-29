class Setting:

    def __init__(self):
        pass

    @staticmethod
    def get_bind(self):
        return {
            'provider': 'mysql',
            'host': 'localhost',
            "user": 'root',
            "password": 'password',
            "database": 'loan_fastapi'
        }

class Setting:

    @staticmethod
    def get_bind(self):
        return {
            'provider': 'mysql',
            'host': 'localhost',
            "user": 'root',
            "password": 'password',
            "database": 'loan_fastapi'
        }

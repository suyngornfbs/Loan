class Setting:

    def __init__(self):
        pass

    @staticmethod
    def get_bind(self):
        return {
            'provider': 'postgres',
            'host': 'localhost',
            'port': 5432,
            'user': 'postgres',
            'password': '069099',
            'database': 'loan_db',
        }

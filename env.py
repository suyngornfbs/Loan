from pony.orm import *

db = Database()
db.bind(provider='mysql', host='localhost', user='root', password='password', database='loan-fast-api')
db.generate_mapping(create_tables=True)
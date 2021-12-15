from datetime import date
import fastapi
from src.router import user, authenticate, customer, disbursement
from src.models.model import Model


app = fastapi.FastAPI(debug=True)
db = Model()


app.include_router(authenticate.router)
app.include_router(user.router)
app.include_router(customer.router)
app.include_router(disbursement.router)


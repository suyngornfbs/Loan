from datetime import date
import fastapi
from src.router import user, authenticate, customer, disbursement, schedule
import uvicorn
from src.models.model import Model


app = fastapi.FastAPI(debug=True)
db = Model()


app.include_router(authenticate.router)
app.include_router(user.router)
app.include_router(customer.router)
app.include_router(disbursement.router)
app.include_router(schedule.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


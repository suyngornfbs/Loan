from datetime import date
import fastapi
from fastapi.staticfiles import StaticFiles
from src.router import user, authenticate, customer, disbursement, schedule, dashboard
import uvicorn
from src.models.model import Model
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI(debug=True)
db = Model()

origins = [
    "*"
]

app.mount('/storage', StaticFiles(directory="storage"), name='storage')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authenticate.router)
app.include_router(dashboard.router)
app.include_router(user.router)
app.include_router(customer.router)
app.include_router(disbursement.router)
app.include_router(schedule.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


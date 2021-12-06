from datetime import date
import fastapi
from src.router import user
from src.models.model import Model


app = fastapi.FastAPI()
db = Model()

app.include_router(user.router)

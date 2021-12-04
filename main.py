from fastapi import FastAPI
import env

app = FastAPI()
env.con()


@app.get("/")
async def root():
    return {"message": "Hello World"}
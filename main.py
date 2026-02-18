from fastapi import FastAPI
app=FastAPI()
from routes import router
app.include_router(router)
@app.get("/")
def root():
    return {"message":"Endpoints working well"}


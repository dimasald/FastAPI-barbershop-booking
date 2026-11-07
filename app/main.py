from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="Barbershop Booking API")

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Barbershop Booking API"}
from fastapi import FastAPI
from app.routers import auth, schedule

app = FastAPI(title="Barbershop Booking API")

app.include_router(auth.router)
app.include_router(schedule.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Barbershop Booking API"}
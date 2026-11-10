from fastapi import FastAPI
from app.routers import auth, schedule, admin

app = FastAPI(title="Barbershop Booking API")

app.include_router(auth.router)
app.include_router(schedule.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Barbershop Booking API"}
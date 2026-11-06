from fastapi import FastAPI

app = FastAPI(title="Barbershop Booking API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Barbershop Booking API"}
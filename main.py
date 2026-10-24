from fastapi import FastAPI

app = FastAPI(title="Restaurant Reservation Engine")

@app.get("/")
def home():
    return {"Status" : "online", "Service" : "Reservation engine"}
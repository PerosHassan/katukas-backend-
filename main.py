from fastapi import FastAPI

app = FastAPI(title="Katukas Kitchen API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Katukas Kitchen Smart Food Ordering API live on Render!"}
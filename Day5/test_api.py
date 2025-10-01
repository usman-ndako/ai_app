from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Ready for Day 5!"}

# To run: uvicorn test_api:app --reload
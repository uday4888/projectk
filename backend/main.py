from fastapi import FastAPI
from items import router as items_router

app = FastAPI(title="ProjectK API")

app.include_router(items_router)


@app.get("/")
def home():
    return {"message": "ProjectK API is running"}
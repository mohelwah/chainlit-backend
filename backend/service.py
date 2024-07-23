from fastapi import APIRouter, FastAPI

from backend.config import config

print(config)
app = FastAPI()

router = APIRouter()


@router.get("/")
async def home():
    return {"Message": "Hello World"}


@router.head("/")
def status_check():
    return {"message": "Site is operational"}


app.include_router(router)

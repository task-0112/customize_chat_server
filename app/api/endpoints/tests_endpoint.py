from fastapi import APIRouter

router = APIRouter()


@router.get("/tests")
async def hello():
    return {"message": "hello"}

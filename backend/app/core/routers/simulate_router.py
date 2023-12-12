from fastapi import APIRouter


router = APIRouter()


@router.get("/start")
def start():
    return {"message": "Simulation started"}


@router.post("/stop")
def stop():
    return {"message": "Simulation ended"}

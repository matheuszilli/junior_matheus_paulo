from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def verificar_saude():
    return {"status": "ok"}

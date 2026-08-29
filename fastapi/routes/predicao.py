from typing import Annotated

from fastapi import APIRouter, Depends

from models.predicao import EntradaPredicao, SaidaPredicao
from security.autenticacao import validar_token


router = APIRouter()


@router.post("/predict", response_model=SaidaPredicao)
def prever_intencao(
    entrada: EntradaPredicao,
    usuario: Annotated[str, Depends(validar_token)],
):
    return SaidaPredicao(intencao="Refund request")

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models.autenticacao import Token
from security.autenticacao import autenticar_admin, criar_token


router = APIRouter()


@router.post("/auth/token", response_model=Token)
def gerar_token(
    formulario: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    if not autenticar_admin(formulario.username, formulario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = criar_token(formulario.username)
    return Token(access_token=token, token_type="bearer")

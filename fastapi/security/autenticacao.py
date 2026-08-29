from datetime import datetime, timedelta, timezone
from secrets import compare_digest
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError


USUARIO_ADMIN = "admin"
SENHA_ADMIN = "infnet"
CHAVE_SECRETA = "Projeto-de-Bloco-Análise-e-Segurança-de-Agentes-de-IA"
ALGORITMO = "HS256"
MINUTOS_EXPIRACAO = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def autenticar_admin(usuario: str, senha: str) -> bool:
    return compare_digest(usuario, USUARIO_ADMIN) and compare_digest(
        senha, SENHA_ADMIN
    )


def criar_token(usuario: str) -> str:
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACAO)
    return jwt.encode(
        {"sub": usuario, "exp": expiracao},
        CHAVE_SECRETA,
        algorithm=ALGORITMO,
    )


def validar_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    erro_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        dados_token = jwt.decode(
            token,
            CHAVE_SECRETA,
            algorithms=[ALGORITMO],
            options={"require": ["sub", "exp"]},
        )
    except InvalidTokenError as erro:
        raise erro_credenciais from erro

    usuario = dados_token.get("sub")
    if usuario != USUARIO_ADMIN:
        raise erro_credenciais

    return usuario

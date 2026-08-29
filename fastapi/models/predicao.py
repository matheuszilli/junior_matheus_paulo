from pydantic import BaseModel, Field


class EntradaPredicao(BaseModel):
    texto: str = Field(min_length=1)


class SaidaPredicao(BaseModel):
    intencao: str

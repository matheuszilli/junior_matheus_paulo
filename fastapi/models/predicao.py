from pydantic import BaseModel, ConfigDict, Field


class EntradaPredicao(BaseModel):
    model_config = ConfigDict(extra="forbid")

    texto: str = Field(min_length=1)


class SaidaPredicao(BaseModel):
    intencao: str

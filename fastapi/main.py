from fastapi import FastAPI

from routes import autenticacao, health, predicao


app = FastAPI(title="Sistema de Atendimento ao Cliente")

app.include_router(health.router)
app.include_router(autenticacao.router)
app.include_router(predicao.router)

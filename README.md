# Projeto de Bloco - TP1

Projeto desenvolvido por Junior, Matheus e Paulo para a disciplina Projeto de Bloco, do bloco Análise e Segurança de Agentes de IA (Instituto Infnet).

## Objetivo do projeto

Construir a base de um sistema de atendimento ao cliente capaz de identificar a intenção da mensagem do usuário. Neste TP1, a entrega cobre:

- a análise exploratória inicial do **Customer Support Ticket Dataset** ([Kaggle](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset)), com **`Ticket Type` definida como variável alvo** do projeto;
- a estrutura base da API em **FastAPI**, com autenticação **JWT** funcional e a rota de predição protegida.

O modelo de machine learning ainda não faz parte desta etapa: a rota `POST /predict` retorna uma intenção pré-determinada que simula a saída do modelo que será implementado nas próximas etapas.

## Estrutura

```text
data/       Dataset utilizado no projeto (customer_support_tickets.csv)
eda/        Notebook com a análise exploratória (customer_support_tickets_eda.ipynb)
fastapi/    Código-fonte da API
  main.py       Ponto de entrada da aplicação
  routes/       Um endpoint por arquivo (health, autenticacao, predicao)
  models/       Modelos Pydantic de entrada e saída
  security/     Geração e validação de JWT, OAuth2PasswordBearer
others/     DFD da API em formato PNG (dfd_api.png) e fonte editável (dfd_api.drawio)
```

## Instalação

Requer **Python 3.11 ou superior**.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

Dependências da API:

```bash
pip install -r fastapi/requirements.txt
```

O arquivo instala `fastapi`, `uvicorn`, `PyJWT` (biblioteca de JWT, instalada à parte do FastAPI) e `python-multipart` (necessário para o formulário do OAuth2).

Dependências do notebook de EDA:

```bash
pip install "pandas>=3.0" matplotlib seaborn notebook
```

O `pandas >= 3.0` é obrigatório: o notebook utiliza o dtype `str` e `select_dtypes(include="str")`, introduzidos no pandas 3 (testado com pandas 3.0.2, matplotlib 3.10 e seaborn 0.13).

## Execução da API

```bash
cd fastapi
uvicorn main:app --reload
```

A documentação interativa (Swagger) estará disponível em `http://127.0.0.1:8000/docs`.

### Rotas

| Rota | Método | Proteção | Descrição |
| ---- | ------ | -------- | --------- |
| `/health` | GET | Nenhuma | Verifica se a API está ativa (`{"status": "ok"}`) |
| `/auth/token` | POST | Credenciais | Autentica o usuário e retorna um token JWT |
| `/predict` | POST | Token JWT | Recebe um texto e retorna a intenção simulada |

### Credenciais de laboratório

Único usuário com acesso à API, definido in-code conforme o enunciado:

| Usuário | Senha    |
| ------- | -------- |
| `admin` | `infnet` |

### Testando a autenticação

No Swagger, execute `POST /auth/token` com as credenciais acima (ou use o botão **Authorize**). O token retornado é um JWT assinado com HS256, com os campos `sub` (usuário) e `exp` (expiração em 30 minutos). Em seguida, chame `POST /predict` com um corpo como:

```json
{
  "texto": "Quero cancelar minha compra"
}
```

Sem token (ou com token inválido/expirado) a rota responde `401`; campos extras no corpo são rejeitados com `422` (`extra="forbid"` no modelo de entrada).

## Execução do notebook de EDA

```bash
cd eda
jupyter notebook customer_support_tickets_eda.ipynb
```

O notebook lê o dataset por caminho relativo (`../data/`), portanto deve ser executado a partir da pasta `eda/`. Ele cobre: compreensão do problema (com a justificativa da variável alvo), inspeção inicial, verificação da qualidade, limpeza e preparação, análise univariada e as hipóteses sobre as intenções dos usuários.

## DFD

O diagrama de fluxo de dados da API está em `others/dfd_api.png`, com as entradas, saídas e trust boundary identificadas e a tríade CIA aplicada a cada componente. O arquivo `others/dfd_api.drawio` é a fonte editável (draw.io / diagrams.net).

## Observações de segurança

Este projeto tem finalidade didática. Para os exercícios, existem simplificações que não devem ser usadas em produção: credenciais e chave JWT definidas no código-fonte, senha sem hash e ausência de TLS. Em uma aplicação real, senhas seriam armazenadas como hash, a chave JWT viria de variável de ambiente ou gerenciador de secrets e o tráfego usaria HTTPS.

## Tecnologias

Python, FastAPI, Pydantic, OAuth2, JWT (PyJWT), Uvicorn, pandas, matplotlib, seaborn.

from fastapi import FastAPI

from database import Database
from model import TransactionRequest
from service import persist_transaction, retrieve_bank_statement

app = FastAPI()
database = Database()


@app.on_event("startup")
async def startup():
    await database.create_pool()


@app.post("/clientes/{user_id}/transacoes")
async def post_transaction(user_id: int, request: TransactionRequest):
    return await persist_transaction(request, user_id, database)


@app.get("/clientes/{user_id}/extrato")
async def get_statement(user_id: int):
    return await retrieve_bank_statement(user_id, database)

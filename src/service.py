import asyncpg
import datetime
from fastapi import HTTPException

from database import Database
from model import TransactionRequest


async def persist_transaction(request: TransactionRequest, user_id: int, db: Database):
    new_value = -request.valor if request.tipo == 'd' else request.valor

    await db.save_transaction(request, user_id)

    try:
        user = await db.update_user_balance(user_id, new_value)
        return {
            "saldo": user['saldo'],
            "limite": user['limite']
        }
    except asyncpg.CheckViolationError:
        raise HTTPException(status_code=422)
    except Exception as e:
        print(e)

async def retrieve_bank_statement(user_id: int, db: Database):
    transactions = await db.select_transactions(user_id)
    user = await db.select_user(user_id)
    if not user:
        raise HTTPException(status_code=404)
    return {
        "saldo": {
            "total": user['saldo'],
            "limite": user['limite'],
            "data_extrato": datetime.datetime.now()
        },
        "ultimas_transacoes": [
            {
                "valor": t['valor'],
                "tipo": t['tipo'],
                "descricao": t['descricao'],
                "realizada_em": t['created_at']
            }
            for t in transactions
        ]
    }

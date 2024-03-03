import os

import asyncpg
from asyncpg import Record

from model import TransactionRequest


class Database:

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOSTNAME"),
            max_size=int(os.getenv("POOL_CONNS"))
        )

    async def select_user(self, user_id: int) -> Record:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                "select saldo, limite from clientes where id=$1",
                user_id
            )

    async def save_transaction(self, request: TransactionRequest, user_id: int):
        async with self.pool.acquire() as conn:
            return await conn.execute(
                "insert into transacoes (user_id, valor, tipo, descricao) values ($1, $2, $3, $4)",
                user_id,
                request.valor,
                request.tipo,
                request.descricao
            )

    async def update_user_balance(self, user_id: int, new_value: int) -> Record:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                "select newbalance as saldo, limit_res as limite from updateUserBalance($1, $2)",
                user_id,
                new_value
            )

    async def select_transactions(self, user_id: int) -> list[Record]:
        async with self.pool.acquire() as conn:
            return await conn.fetch(
                "select valor, tipo, descricao, created_at from transacoes where user_id = $1 order by id desc limit 10",
                user_id
            )

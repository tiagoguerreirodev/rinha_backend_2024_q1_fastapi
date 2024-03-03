import datetime

from asyncpg import Record
from pydantic import BaseModel, Field
from typing import Literal


class TransactionRequest(BaseModel):
    valor: int
    tipo: Literal['c', 'd']
    descricao: str = Field(min_length=1, max_length=10)


class User(Record):
    saldo: int
    limite: int


class Transaction(Record):
    valor: int
    tipo: str
    descricao: str
    created_at: datetime.datetime

-- Coloque scripts iniciais aqui
CREATE UNLOGGED TABLE clientes (
    id SMALLINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    limite INTEGER,
    saldo INTEGER DEFAULT 0
);

CREATE INDEX idx_client_id ON clientes USING HASH(id);

ALTER TABLE clientes ADD CONSTRAINT balance_within_limit CHECK (saldo > -limite);

CREATE UNLOGGED TABLE transacoes (
    id INT GENERATED BY DEFAULT AS IDENTITY,
    user_id SMALLINT,
    valor INTEGER,
    tipo VARCHAR(1),
    descricao VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transaction_id_desc ON transacoes (id DESC);
CREATE INDEX idx_transaction_user_id ON transacoes USING HASH(user_id);

-- Função para atualizar o saldo do usuário
CREATE OR REPLACE FUNCTION updateUserBalance(userId SMALLINT, transactionValue INTEGER)
    RETURNS TABLE (newBalance INTEGER, limit_res INTEGER)
AS $$
DECLARE
    old_balance INTEGER;
    new_balance INTEGER;
    limit_res INTEGER;
BEGIN
    SELECT saldo, limite INTO old_balance, limit_res FROM clientes WHERE id = userId FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'user not found on postgres';
    END IF;

    SELECT transactionValue + old_balance INTO new_balance;
    UPDATE clientes SET saldo = new_balance WHERE id = userId;
    RETURN QUERY SELECT new_balance, limit_res;
END;
    $$ LANGUAGE plpgsql;

DO $$
BEGIN
  INSERT INTO clientes (limite)
  VALUES
    (1000 * 100),
    (800 * 100),
    (10000 * 100),
    (100000 * 100),
    (5000 * 100);
END;
    $$
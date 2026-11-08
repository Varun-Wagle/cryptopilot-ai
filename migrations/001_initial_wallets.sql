CREATE TABLE IF NOT EXISTS wallets (
    id UUID PRIMARY KEY,
    label VARCHAR(80) NOT NULL CHECK (length(btrim(label)) BETWEEN 1 AND 80),
    chain_family VARCHAR(30) NOT NULL CHECK (chain_family IN ('evm', 'solana', 'bitcoin', 'other')),
    network VARCHAR(80) NOT NULL CHECK (length(btrim(network)) BETWEEN 2 AND 80),
    address VARCHAR(200) NOT NULL CHECK (length(btrim(address)) BETWEEN 8 AND 200),
    address_normalized VARCHAR(200) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_wallet_network_address UNIQUE (network, address_normalized)
);
CREATE INDEX IF NOT EXISTS wallets_active_created_at_idx ON wallets (is_active, created_at DESC);
CREATE INDEX IF NOT EXISTS wallets_chain_family_network_idx ON wallets (chain_family, network);

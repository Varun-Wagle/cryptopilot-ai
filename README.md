# CryptoPilot AI — Phase 1

Dockerized FastAPI + PostgreSQL foundation for a multi-chain crypto opportunity and earnings platform.

## Scope
- FastAPI backend and PostgreSQL
- SQL migration runner
- Public wallet registration/listing (EVM, Solana, Bitcoin, other)
- Health/readiness endpoints
- No private keys, signing, transfers, mining, or reward claims

## Requirements
- Docker Desktop with Docker Compose
- Copy `.env.example` to `.env`
- Set a strong `POSTGRES_PASSWORD` and make the same password match the password in `DATABASE_URL`.

## Start
```powershell
Copy-Item .env.example .env
# Edit .env and replace both occurrences of CHANGE_ME...
docker compose up --build -d
```
Open:
- http://localhost:8000/health
- http://localhost:8000/ready
- http://localhost:8000/docs

Logs: `docker compose logs -f api`
Stop: `docker compose down`
Destructive reset (deletes local DB data): `docker compose down -v`

## Register a public wallet
POST `/api/v1/wallets`
```json
{
  "label": "Main EVM public wallet",
  "chain_family": "evm",
  "network": "ethereum",
  "address": "0x1111111111111111111111111111111111111111"
}
```
The address is an illustrative placeholder, not a wallet recommendation or ownership proof.

## Endpoints
| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Process liveness |
| GET | `/ready` | Database readiness |
| POST | `/api/v1/wallets` | Register public wallet |
| GET | `/api/v1/wallets` | List wallets |
| GET | `/api/v1/wallets/{wallet_id}` | Retrieve wallet |
| PATCH | `/api/v1/wallets/{wallet_id}/deactivate` | Deactivate wallet |

## Security
- Store public addresses only. Never provide seed phrases, private keys, or keystore files.
- Registration does not prove wallet ownership.
- No transaction signing or asset movement is implemented.
- PostgreSQL is not published to the host.
- Before internet exposure, add authentication, authorization, HTTPS, rate limits, backups, and managed secrets.

## Limitations
Address validation is basic format validation, not chain-specific checksum or ownership verification. No live balances or rewards are fetched yet. A chain registry and chain adapters come in a later phase.

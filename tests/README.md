# Manual smoke tests
1. Open `/docs`.
2. Call `GET /health` and `GET /ready`.
3. Register a public address with `POST /api/v1/wallets`.
4. Confirm it appears in `GET /api/v1/wallets`.
5. Register the same network/address again; expect HTTP 409.
6. Deactivate it and verify it is omitted from the default active-only listing.

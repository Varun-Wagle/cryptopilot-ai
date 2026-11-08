import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.wallet import Wallet
from app.schemas.wallet import WalletCreate, WalletList, WalletRead

router = APIRouter(prefix="/api/v1/wallets", tags=["wallets"])

@router.post("", response_model=WalletRead, status_code=status.HTTP_201_CREATED)
def create_wallet(payload: WalletCreate, db: Session = Depends(get_db)):
    normalized = payload.address.lower() if payload.chain_family == "evm" else payload.address
    wallet = Wallet(
        label=payload.label, chain_family=payload.chain_family, network=payload.network,
        address=payload.address, address_normalized=normalized,
    )
    db.add(wallet)
    try:
        db.commit()
        db.refresh(wallet)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Address already registered for this network.")
    return wallet

@router.get("", response_model=WalletList)
def list_wallets(
    active_only: bool = Query(default=True),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    query = select(Wallet)
    count_query = select(func.count()).select_from(Wallet)
    if active_only:
        query = query.where(Wallet.is_active.is_(True))
        count_query = count_query.where(Wallet.is_active.is_(True))
    total = db.scalar(count_query) or 0
    items = db.scalars(query.order_by(Wallet.created_at.desc()).limit(limit).offset(offset)).all()
    return {"items": items, "total": total}

@router.get("/{wallet_id}", response_model=WalletRead)
def get_wallet(wallet_id: uuid.UUID, db: Session = Depends(get_db)):
    wallet = db.get(Wallet, wallet_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@router.patch("/{wallet_id}/deactivate", response_model=WalletRead)
def deactivate_wallet(wallet_id: uuid.UUID, db: Session = Depends(get_db)):
    wallet = db.get(Wallet, wallet_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    wallet.is_active = False
    db.commit()
    db.refresh(wallet)
    return wallet

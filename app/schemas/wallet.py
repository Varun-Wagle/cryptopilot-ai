import uuid
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

class WalletCreate(BaseModel):
    label: str = Field(min_length=1, max_length=80)
    chain_family: Literal["evm", "solana", "bitcoin", "other"]
    network: str = Field(min_length=2, max_length=80)
    address: str = Field(min_length=8, max_length=200)

    @field_validator("label", "network", "address")
    @classmethod
    def strip_nonblank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be blank")
        return value

    @field_validator("network")
    @classmethod
    def normalize_network(cls, value: str) -> str:
        return value.lower()

    @field_validator("address")
    @classmethod
    def reject_whitespace(cls, value: str) -> str:
        if any(ch.isspace() for ch in value):
            raise ValueError("Address cannot contain whitespace")
        return value

class WalletRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    label: str
    chain_family: str
    network: str
    address: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

class WalletList(BaseModel):
    items: list[WalletRead]
    total: int

"""Pydantic models (request / response schemas)."""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ---------- Users ----------
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr


# ---------- Orders ----------
class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    cancelled = "cancelled"


class OrderCreate(BaseModel):
    user_id: int
    product: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderOut(BaseModel):
    id: int
    user_id: int
    product: str
    quantity: int
    price: float
    status: OrderStatus
    created_at: datetime

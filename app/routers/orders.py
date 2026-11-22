"""Order APIs."""
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from app import database as db
from app.schemas import OrderCreate, OrderOut, OrderStatus, OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])


def _get_order_or_404(order_id: int) -> dict:
    order = db.orders_db.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate):
    """Create an order for an existing user."""
    if payload.user_id not in db.users_db:
        raise HTTPException(status_code=404, detail="User not found")

    order_id = next(db.order_id_seq)
    order = {
        "id": order_id,
        **payload.model_dump(),
        "status": OrderStatus.pending,
        "created_at": datetime.now(timezone.utc),
    }
    db.orders_db[order_id] = order
    return order


@router.get("", response_model=list[OrderOut])
def list_orders(user_id: int | None = None, status_filter: OrderStatus | None = None):
    """List orders. Optionally filter by user_id and/or status."""
    orders = list(db.orders_db.values())

    if user_id is not None:
        orders = [o for o in orders if o["user_id"] == user_id]
    if status_filter is not None:
        orders = [o for o in orders if o["status"] == status_filter]

    return orders


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int):
    """Get a single order by ID."""
    return _get_order_or_404(order_id)


@router.patch("/{order_id}/status", response_model=OrderOut)
def update_order_status(order_id: int, payload: OrderStatusUpdate):
    """Update the status of an order (pending -> paid -> shipped, or cancelled)."""
    order = _get_order_or_404(order_id)
    order["status"] = payload.status
    return order

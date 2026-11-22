"""User APIs."""
from fastapi import APIRouter, HTTPException, status

from app import database as db
from app.schemas import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


def _get_user_or_404(user_id: int) -> dict:
    user = db.users_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def _email_taken(email: str, exclude_id: int | None = None) -> bool:
    return any(
        u["email"].lower() == email.lower() and u["id"] != exclude_id
        for u in db.users_db.values()
    )


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    """Create a new user."""
    if _email_taken(payload.email):
        raise HTTPException(status_code=409, detail="Email already registered")

    user_id = next(db.user_id_seq)
    user = {"id": user_id, **payload.model_dump()}
    db.users_db[user_id] = user
    return user


@router.get("", response_model=list[UserOut])
def list_users():
    """List all users."""
    return list(db.users_db.values())


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    """Get a single user by ID."""
    return _get_user_or_404(user_id)


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate):
    """Partially update a user (only the fields sent are changed)."""
    user = _get_user_or_404(user_id)
    updates = payload.model_dump(exclude_none=True)

    if "email" in updates and _email_taken(updates["email"], exclude_id=user_id):
        raise HTTPException(status_code=409, detail="Email already registered")

    user.update(updates)
    return user

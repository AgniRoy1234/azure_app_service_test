"""In-memory storage shared by the routers (swap for a real DB later)."""
from itertools import count

users_db: dict[int, dict] = {}
orders_db: dict[int, dict] = {}

user_id_seq = count(1)
order_id_seq = count(1)

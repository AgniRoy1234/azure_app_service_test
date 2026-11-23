"""Application entry point.

Run with:
    uvicorn main:app --reload
Docs:
    http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI

from app.routers import orders, users

app = FastAPI(title="Users & Orders API", version="1.0.0")

app.include_router(users.router)
app.include_router(orders.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}

# if __name__ == "__main__":
#   import uvicorn
#   uvicorn.run(app, host="localhost", port=8000)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
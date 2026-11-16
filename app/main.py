from fastapi import FastAPI

from app.api import talk

app = FastAPI()


app.include_router(talk.router)


@app.get("/")
async def root() -> dict[str, str]:
    """Return a fixed message, to check that the service is up."""
    return {"message": "Test!"}

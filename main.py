from datetime import datetime

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


api_url = "/api/v1/health"


@app.get(api_url)
def health_check():
    status = "ok"
    version = api_url.split("/")[2]
    timestamp = datetime.now().isoformat()

    return {
        "status": status,
        "version": version,
        "timestamp": timestamp,
    }

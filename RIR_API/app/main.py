"""RIR-API - Room Impulse Response API.

Punto de entrada de la aplicacion FastAPI.

Uso:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routers import signals, filters, acoustics, analysis, utils, health
from app.web.home import HOME_PAGE


app = FastAPI(
    title="RIR-API",
    description=(
        "API para procesamiento y analisis de respuestas al impulso "
        "segun ISO 3382."
    ),
    version="0.1.0",
)

# Routers
app.include_router(health.router)
app.include_router(signals.router)
app.include_router(filters.router)
app.include_router(acoustics.router)
app.include_router(analysis.router)
app.include_router(utils.router)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    """Página de inicio de la API."""
    return HOME_PAGE


API_VERSION = "0.1.0"
API_URL_VERSION = "v1"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

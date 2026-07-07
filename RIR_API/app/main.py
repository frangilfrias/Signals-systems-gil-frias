"""RIR-API - Room Impulse Response API.

Punto de entrada de la aplicacion FastAPI.

Uso:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routers import signals, filters, acoustics, analysis, utils, health


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
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>RIR-API</title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #1e1e2f, #2a2a40);
                color: #f0f0f0;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                text-align: center;
            }
            .card {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 16px;
                padding: 2.5rem 3rem;
                box-shadow: 0 8px 32px rgba(0,0,0,0.4);
                backdrop-filter: blur(6px);
            }
            h1 {
                margin: 0 0 0.3rem;
                font-size: 1.8rem;
                color: #8ecae6;
            }
            h2 {
                margin: 0 0 1.5rem;
                font-weight: 400;
                font-size: 1.1rem;
                color: #bbb;
            }
            .integrantes {
                list-style: none;
                padding: 0;
                margin: 0 0 1.5rem;
            }
            .integrantes li {
                padding: 0.2rem 0;
                font-size: 0.95rem;
            }
            a {
                color: #8ecae6;
                text-decoration: none;
                font-size: 0.9rem;
            }
            a:hover {
                text-decoration: underline;
            }
            .badge {
                display: inline-block;
                margin-top: 1rem;
                padding: 0.3rem 0.8rem;
                border-radius: 999px;
                background: rgba(142, 202, 230, 0.15);
                color: #8ecae6;
                font-size: 0.75rem;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Trabajo Práctico - Señales y Sistemas</h1>
            <h2>Grupo 1</h2>
            <ul class="integrantes">
                <li>Mora Sawczyk </li>
                <li>Matias Moreira </li>
                <li>Francisco Gil Frias </li>
            </ul>
            <a href="/docs">Ver documentación de la API →</a>
            <div class="badge">RIR-API · v0.1.0</div>
        </div>
    </body>
    </html>
    """


API_VERSION = "0.1.0"
API_URL_VERSION = "v1"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

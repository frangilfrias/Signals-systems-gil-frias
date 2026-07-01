"""RIR-API - Room Impulse Response API.

Punto de entrada de la aplicacion FastAPI.

Uso:
    uvicorn app.main:app --reload
"""

import io
from datetime import UTC, datetime

import soundfile as sf
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse

from app.routers import health
from app.services.pink_noise import generar_ruido_rosa

app = FastAPI(
    title="RIR-API",
    description="API para procesamiento y analisis de respuestas al impulso segun ISO 3382.",
    version="0.1.0",
)

# Routers
app.include_router(health.router)

# TODO (M3): Agregar routers de signals, filters, acoustics, analysis, utils
# app.include_router(signals.router, prefix="/api/v1/signals", tags=["signals"])
# app.include_router(filters.router, prefix="/api/v1/filters", tags=["filters"])
# app.include_router(acoustics.router, prefix="/api/v1/acoustics", tags=["acoustics"])
# app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
# app.include_router(utils.router, prefix="/api/v1/utils", tags=["utils"])


@app.get("/", response_class=HTMLResponse)
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


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": API_VERSION,
        "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    }


@app.post("/api/v1/signals/pink-noise")
async def pink_noise(duracion: float = 1.0, fs: int = 44100):
    ruido_rosa = generar_ruido_rosa(duracion, fs)

    buffer = io.BytesIO()
    sf.write(buffer, ruido_rosa, fs, format="WAV")
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="audio/wav",
        headers={"Content-Disposition": "attachment; filename=pink_noise.wav"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

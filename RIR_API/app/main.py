"""RIR-API - Room Impulse Response API.

Punto de entrada de la aplicacion FastAPI.

Uso:
    uvicorn app.main:app --reload
"""

import io
from datetime import UTC, datetime

import numpy as np
import soundfile as sf
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse

from app.routers import health
from app.services.acoustic_parameters import (
    calcular_parametros_acusticos,
    integral_schroeder,
    suavizar_signal,
)
from app.services.filter import filtro_octava
from app.services.pink_noise import generar_ruido_rosa
from app.services.signal_utils import a_escala_log, sintetizar_ri
from app.services.sine_sweep import generar_sine_sweep

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


@app.post("/api/v1/signals/sine-sweep")
async def sine_sweep(
    f1: float = 20,
    f2: float = 20000,
    duracion: float = 5.0,
    fs: int = 44100,
):
    sweep, _ = generar_sine_sweep(f1, f2, duracion, fs)

    buffer = io.BytesIO()
    sf.write(buffer, sweep, fs, format="WAV")
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="audio/wav",
        headers={"Content-Disposition": "attachment; filename=sine_sweep.wav"},
    )


@app.post("/api/v1/signals/synthetic-ir")
async def synthetic_ir(
    fs: int = 44100,
    duracion: float = 3.0,
):
    """
    Genera una respuesta al impulso sintética a partir de
    tiempos de reverberación por banda.
    """

    t60_por_banda = {
        125: 1.2,
        250: 1.1,
        500: 1.0,
        1000: 0.9,
        2000: 0.8,
        4000: 0.7,
    }

    rir = sintetizar_ri(
        t60_por_banda=t60_por_banda,
        fs=fs,
        duracion=duracion,
    )

    buffer = io.BytesIO()
    sf.write(buffer, rir, fs, format="WAV")
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="audio/wav",
        headers={
            "Content-Disposition": (
                "attachment; "
                "filename=synthetic_ir.wav"
            ),
        },
    )


@app.post("/api/v1/filters/band")
async def filtro_banda(
    archivo: UploadFile = File(...),
    fc: float = 1000.0,
    orden: int = 4,
):
    """
    Filtra un archivo de audio mediante un filtro pasabanda de octava.
    """

    # Leer el archivo recibido
    datos = await archivo.read()

    buffer = io.BytesIO(datos)

    signal, fs = sf.read(buffer, dtype="float64")

    # Si es estéreo -> convertir a mono
    if signal.ndim > 1:
        signal = np.mean(signal, axis=1)

    # Aplicar filtro
    filtrada = filtro_octava(
        signal=signal,
        fc=fc,
        fs=fs,
        orden=orden,
    )

    # Guardar resultado en memoria
    salida = io.BytesIO()

    sf.write(
        salida,
        filtrada,
        fs,
        format="WAV",
    )

    salida.seek(0)

    return StreamingResponse(
        salida,
        media_type="audio/wav",
        headers={
            "Content-Disposition": (
                f"attachment; filename=band_{int(fc)}Hz.wav"
            )
        },
    )


@app.get("/api/v1/filters/frequencies")
async def frecuencias_centrales():
    """
    Devuelve las frecuencias centrales de las bandas de octava soportadas.
    """

    return {
        "frequencies_hz": [
            31.5,
            63,
            125,
            250,
            500,
            1000,
            2000,
            4000,
            8000,
            16000,
        ]
    }


@app.post("/api/v1/acoustics/parameters")
async def acoustic_parameters(file: UploadFile = File(...)):
    """
    Calcula los parámetros acústicos de una respuesta al impulso.
    """

    if not file.filename.lower().endswith((".wav", ".flac")):
        raise HTTPException(
            status_code=400,
            detail="Solo se aceptan archivos WAV o FLAC.",
        )

    try:
        signal, fs = sf.read(file.file)

        # Si es estéreo → convertir a mono
        if signal.ndim == 2:
            signal = signal.mean(axis=1)

        parametros = calcular_parametros_acusticos(signal, fs)

        return {
            "sample_rate": fs,
            "parameters": parametros,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.post("/api/v1/acoustics/parameters/by-bands")
async def acoustic_parameters_by_bands(file: UploadFile = File(...)):
    """
    Calcula los parámetros acústicos agrupados por banda de octava.
    """

    if not file.filename.lower().endswith((".wav", ".flac")):
        raise HTTPException(
            status_code=400,
            detail="Solo se aceptan archivos WAV o FLAC.",
        )

    try:
        signal, fs = sf.read(file.file)

        if signal.ndim == 2:
            signal = signal.mean(axis=1)

        parametros = calcular_parametros_acusticos(signal, fs)

        bandas = {}

        for parametro, valores in parametros.items():
            for fc, valor in valores.items():
                bandas.setdefault(fc, {})
                bandas[fc][parametro] = valor

        return {
            "sample_rate": fs,
            "bands": bandas,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.post("/api/v1/analysis/impulse-response")
async def analizar_respuesta_impulso(file: UploadFile = File(...)):
    """
    Realiza un análisis completo de una respuesta al impulso.
    """

    if not file.filename.lower().endswith((".wav", ".flac")):
        raise HTTPException(
            status_code=400,
            detail="Solo se aceptan archivos WAV o FLAC.",
        )

    try:
        signal, fs = sf.read(file.file)

        # Convertir a mono si corresponde
        if signal.ndim == 2:
            signal = signal.mean(axis=1)

        # Curva de Schroeder
        edc = integral_schroeder(signal)
        edc_db = a_escala_log(edc)

        # Parámetros acústicos
        parametros = calcular_parametros_acusticos(signal, fs)

        return {
            "sample_rate": fs,
            "samples": len(signal),
            "duration": len(signal) / fs,
            "schroeder_points": len(edc_db),
            "schroeder_preview": edc_db[:200].tolist(),
            "acoustic_parameters": parametros,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.post("/api/v1/utils/schroeder")
async def schroeder(file: UploadFile = File(...)):
    """
    Calcula la Integral de Schroeder de una respuesta al impulso.
    """

    if not file.filename.lower().endswith((".wav", ".flac")):
        raise HTTPException(
            status_code=400,
            detail="Solo se aceptan archivos WAV o FLAC.",
        )

    try:
        signal, fs = sf.read(file.file)

        if signal.ndim == 2:
            signal = signal.mean(axis=1)

        edc = integral_schroeder(signal)

        return {
            "sample_rate": fs,
            "samples": len(signal),
            "schroeder_points": len(edc),
            "schroeder_preview": edc[:200].tolist(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.post("/api/v1/utils/smoothing")
async def smoothing(
    file: UploadFile = File(...),
    method: str = Query(default="hilbert"),
    window_ms: int = Query(default=10, ge=1, le=100),
):
    """
    Aplica suavizado a una señal de audio.

    Métodos disponibles:
    - hilbert
    - moving_average (media móvil)
    """

    if not file.filename.lower().endswith((".wav", ".flac")):
        raise HTTPException(
            status_code=400,
            detail="Solo se aceptan archivos WAV o FLAC.",
        )

    try:
        signal, fs = sf.read(file.file)

        # Convertir estéreo a mono
        if signal.ndim == 2:
            signal = signal.mean(axis=1)

        # Elegir método
        if method == "hilbert":
            smoothed = suavizar_signal(signal, "hilbert")
            window_samples = None

        elif method == "moving_average":
            window_samples = max(1, int(window_ms * fs / 1000))
            smoothed = suavizar_signal(signal, window_samples)
        else:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Método inválido. "
                    "Opciones: 'hilbert' o 'moving_average'."
                ),
            )

        return {
            "method": method,
            "window_ms": window_ms,
            "num_samples": len(smoothed),
            "file_path": file.filename,
            "signal_preview": smoothed[:200].tolist(),
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.post("/api/v1/utils/log-scale")
async def log_scale(file: UploadFile = File(...)):
    """
    Convierte una señal a escala logarítmica (dB).
    """

    if not file.filename.lower().endswith((".wav", ".flac")):
        raise HTTPException(
            status_code=400,
            detail="Solo se aceptan archivos WAV o FLAC.",
        )

    try:
        signal, fs = sf.read(file.file)

        # Convertir a mono si el archivo es estéreo
        if signal.ndim == 2:
            signal = signal.mean(axis=1)

        signal_db = a_escala_log(signal)

        return {
            "num_samples": len(signal_db),
            "min_db": float(signal_db.min()),
            "max_db": float(signal_db.max()),
            "file_path": file.filename,
            "signal_db_preview": signal_db[:200].tolist(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

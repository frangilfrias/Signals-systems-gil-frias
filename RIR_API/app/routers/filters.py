import io

import numpy as np
import soundfile as sf

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse

from app.services.filter import filtro_octava

router = APIRouter(
    prefix="/api/v1/filters",
    tags=["Filters"],
)
@router.post("/band")
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


@router.get("/frequencies")
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

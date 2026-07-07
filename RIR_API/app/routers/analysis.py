import soundfile as sf

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.acoustic_parameters import (
    calcular_parametros_acusticos,
    integral_schroeder,
)
from app.services.signal_utils import a_escala_log

router = APIRouter(
    prefix="/api/v1/analysis",
    tags=["Analysis"],
)


@router.post("/impulse-response")
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

import soundfile as sf

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.acoustic_parameters import (
    calcular_parametros_acusticos,
)

router = APIRouter(
    prefix="/api/v1/acoustics",
    tags=["Acoustics"],
)


@router.post("/parameters")
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


@router.post("/by-bands")
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

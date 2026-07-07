import soundfile as sf

from fastapi import APIRouter, File, HTTPException, UploadFile, Query

from app.services.acoustic_parameters import integral_schroeder, suavizar_signal
from app.services.signal_utils import a_escala_log

router = APIRouter(
    prefix="/api/v1/utils",
    tags=["Utils"],
)


@router.post("/schroeder")
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


@router.post("/smoothing")
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


@router.post("/log-scale")
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

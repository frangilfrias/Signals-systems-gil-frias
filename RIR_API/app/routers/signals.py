from fastapi import APIRouter
import io
import soundfile as sf

from fastapi.responses import StreamingResponse
from app.services.pink_noise import generar_ruido_rosa
from app.services.sine_sweep import generar_sine_sweep
from app.services.signal_utils import sintetizar_ri

router = APIRouter(
    prefix="/api/v1/signals",
    tags=["Signals"],
)


@router.post("/pink-noise")
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


@router.post("/sine-sweep")
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


@router.post("/synthetic-ir")
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

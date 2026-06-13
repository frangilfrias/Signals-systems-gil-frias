"""Utilidades de procesamiento de senales.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

from pathlib import Path

import numpy as np
import soundfile as sf


def cargar_audio(ruta: str | Path) -> tuple[np.ndarray, int]:
    """
    Carga un archivo de audio WAV o FLAC.

    Parameters
    ----------
    ruta : str | Path
        Ruta al archivo de audio.

    Returns
    -------
    tuple[np.ndarray, int]
        Tupla con (senal, frecuencia_de_muestreo).
        La senal se devuelve como float64 normalizada entre -1 y 1.
        Si el audio es estereo, shape = (n_muestras, n_canales).

    Raises
    ------
    FileNotFoundError
        Si el archivo no existe.
    ValueError
        Si el formato no es soportado (solo WAV o FLAC).
    """
    ruta = Path(ruta)

    if not ruta.exists():
        raise FileNotFoundError(f"No se encontro el archivo: {ruta}")

    extension = ruta.suffix.lower()
    if extension not in (".wav", ".flac"):
        raise ValueError(f"Formato '{extension}' no soportado. Usar WAV o FLAC.")

    senal, sample_rate = sf.read(ruta, dtype="float64")

    maximo = np.max(np.abs(senal))
    if maximo > 0:
        senal = senal / maximo

    return senal, sample_rate

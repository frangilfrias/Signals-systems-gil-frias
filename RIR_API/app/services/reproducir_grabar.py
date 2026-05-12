import numpy as np
import sounddevice as sd


def reproducir_y_grabar(signal: np.ndarray, fs: int, duracion_grabacion: float) -> np.ndarray:
    cantidad_frames = int(duracion_grabacion * fs)
    grabacion = sd.rec(cantidad_frames, fs, 1)
    sd.play(signal, fs)
    sd.wait()
    return grabacion.flatten()

    """
    Reproduce una senal y graba simultaneamente.

    Parameters
    ----------
    signal : np.ndarray
        Senal a reproducir.
    fs : int
        Frecuencia de muestreo en Hz.
    duracion_grabacion : float
        Duracion total de la grabacion en segundos.
        Debe ser >= duracion de la senal para capturar la reverberacion.

    Returns
    -------
    np.ndarray
        Array con la senal grabada.
    """

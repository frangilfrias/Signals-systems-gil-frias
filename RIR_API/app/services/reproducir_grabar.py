import numpy as np
import sounddevice as sd


def reproducir_y_grabar(
    signal: np.ndarray, fs: int, duracion_grabacion: float, preroll: float = 0.7
) -> np.ndarray:
    """
    Reproduce una señal y graba simultáneamente en modo full-duplex.

    Parameters
    ----------
    signal : np.ndarray
        Señal a reproducir (mono o estéreo).
    fs : int
        Frecuencia de muestreo.
    duracion_grabacion : float
        Duración total de la grabación (s).
    preroll : float
        Silencio inicial (s) para compensar latencia.

    Returns
    -------
    np.ndarray
        Señal grabada.
    """
    try:
        sd.query_devices()
    except Exception as e:
        raise RuntimeError(f"No hay dispositivos de audio disponibles: {e}")

    if signal.ndim == 1:
        signal = signal[:, np.newaxis]

    n_channels = signal.shape[1]
    preroll_samples = int(preroll * fs)
    silencio = np.zeros((preroll_samples, n_channels))
    signal_out = np.vstack([silencio, signal])
    total_frames = int(duracion_grabacion * fs)

    if total_frames < len(signal_out):
        raise ValueError("La duración de grabación es insuficiente.")

    padding = total_frames - len(signal_out)

    if padding > 0:
        signal_out = np.vstack([signal_out, np.zeros((padding, n_channels))])

    grabacion = sd.playrec(signal_out, samplerate=fs, channels=n_channels)
    sd.wait()

    return grabacion

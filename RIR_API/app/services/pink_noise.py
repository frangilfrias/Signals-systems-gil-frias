"""Servicio de generacion de ruido rosa.

Milestone 1: Generacion de senales."""

import numpy as np


def generar_ruido_rosa(duracion: float, fs: int) -> np.ndarray:
    """
    Genera una señal de ruido rosa de la duración especificada.

    El ruido rosa tiene una densidad espectral de potencia inversamente
    proporcional a la frecuencia (1/f). Esto significa que cada octava
    contiene la misma cantidad de energía, lo cual lo hace útil para
    mediciones acústicas.

    Algoritmo implementado
    ----------------------
    1. Generar ruido blanco (distribución normal) de la duración deseada.
    2. Aplicar la transformada de Fourier (`np.fft.rfft`).
    3. Crear un vector de frecuencias correspondiente.
    4. Dividir cada componente por sqrt(f) (omitir f=0 para evitar división
       por cero).
    5. Aplicar la transformada inversa (`np.fft.irfft`).
    6. Normalizar la señal resultante al rango [-1, 1].

    Parameters
    ----------
    duracion : float
        Duración de la señal en segundos.

    fs : int
        Frecuencia de muestreo en Hz.

    Returns
    -------
    np.ndarray
         Señal de ruido rosa normalizada, de longitud
        ``int(duracion * fs)``.
    """
    # Validación de tipo (runtime) de entrada 
    if not isinstance(duracion, float):
        raise TypeError(f"duracion debe ser numérica (float). Tipo recibido: {type(duracion).__name__}, valor: {duracion}")
    if not isinstance(fs, int):
        raise TypeError(f"fs debe ser numérica (int). Tipo recibido: {type(fs).__name__}, valor: {fs}")
    
    # Validación de valores de entrada
    fs_validas = {44100, 48000, 88200, 96000, 176400, 192000, 352800, 384000, 705600, 768000}

    if fs not in fs_validas:
        raise ValueError(f"fs invalida: {fs}. Valores permitidos: {fs_validas}")

    # Generar ruido blanco (distribución normal) de la duración deseada
    n_muestras = int(fs * duracion)
    ruido_blanco = np.random.randn(n_muestras)

    # Aplicar la transformada de Fourier
    espectro = np.fft.rfft(ruido_blanco)

    # Crear vector de frecuencias
    freqs = np.fft.rfftfreq(n_muestras, d=1 / fs)

    # Dividir cada componente por sqrt(f)
    # Se omite f=0 para evitar división por cero
    espectro[1:] = espectro[1:] / np.sqrt(freqs[1:])

    # Aplicar transformada inversa
    ruido_rosa = np.fft.irfft(espectro)

    # Normalización [-1, 1]
    ruido_rosa = ruido_rosa / np.max(np.abs(ruido_rosa))

    return ruido_rosa

    
fs = 192000
duracion = 30.0

ruido_rosa = generar_ruido_rosa(duracion, fs)

print(ruido_rosa)
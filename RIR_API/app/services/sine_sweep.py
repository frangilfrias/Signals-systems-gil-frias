import numpy as np

def generar_sine_sweep(
    f1: float, f2: float, duracion: float, fs: int
) -> tuple[np.ndarray, np.ndarray]:
    """Genera un barrido senoidal logaritmico (sine sweep) y su filtro inverso.
    El sine sweep logaritmico es la senal de excitacion preferida para
    la medicion de respuestas al impulso segun la tecnica de Farina (2000).

    Parameters
    ----------
    f1 : float
        Frecuencia inicial del barrido en Hz (tipicamente 20 Hz).
    f2 : float
        Frecuencia final del barrido en Hz (tipicamente 20000 Hz).
    duracion : float
        Duracion del barrido en segundos.
    fs : int
        Frecuencia de muestreo en Hz.

    Returns
    -------
    sweep : np.ndarray
        Senal del barrido senoidal.
    filtro_inverso : np.ndarray
        Filtro inverso correspondiente.

    References
    ----------
    .. [1] Farina, A. (2000). "Simultaneous measurement of impulse response
       and distortion with a swept-sine technique."
    """
    ###Validación de datos:

    fs_validas = [44100, 48000, 88200, 96000, 176400, 192000, 352800, 384000, 705600, 768000]

    #Validación de tipo

    if not isinstance(f1, (int, float)):
        raise TypeError(
            f"f1 debe ser int o float. "
            f"Tipo recibido: {type(f1).__name__}, valor: {f1}"
        )

    if not isinstance(f2, (int, float)):
        raise TypeError(
            f"f2 debe ser int o float. "
            f"Tipo recibido: {type(f2).__name__}, valor: {f2}"
        )

    if not isinstance(duracion, (int, float)):
        raise TypeError(
            f"duracion debe ser int o float. "
            f"Tipo recibido: {type(duracion).__name__}, valor: {duracion}"
        )

    if not isinstance(fs, int):
        raise TypeError(
            f"fs debe ser int. "
            f"Tipo recibido: {type(fs).__name__}, valor: {fs}"
        )

    #Validación de valor

    if f1 <= 0:
        raise ValueError(
            "f1 debe ser mayor que 0 Hz."
        )

    if f2 <= 0:
        raise ValueError(
            "f2 debe ser mayor que 0 Hz."
        )

    if f1 >= f2:
        raise ValueError(
            "f1 debe ser menor que f2."
        )

    if duracion <= 0:
        raise ValueError(
            "La duración debe ser mayor que 0 segundos."
        )

    if fs not in fs_validas:
        raise ValueError(
            f"fs inválida: {fs}. "
            f"Valores permitidos: {fs_validas}"
        )

    #Genero la cantidad de muestras y el vector del eje temporal para el sweep
    num_muestras = int(duracion*fs)
    eje_tem = np.arange(num_muestras)/fs

    #Creo un parametro para facilitar la escritura de la fórmula
    k_param = duracion / np.log(f2/f1)

    #Genero el sweep con los parámetros establecidos
    sweep = np.sin( 2 * np.pi * f1 * k_param * (np.exp(eje_tem/k_param)-1))

    #Produzco el filtro inverso
    compensacion_temp = np.exp(-eje_tem/k_param) # Compensa la distribución no uniforme de energía del sweep logarítmico
    filtro_inv = sweep[::-1] * compensacion_temp

    #Normalizo ambos vectores
    sweep /= np.max(np.abs(sweep))
    filtro_inv /= np.max(np.abs(filtro_inv))

    return sweep , filtro_inv





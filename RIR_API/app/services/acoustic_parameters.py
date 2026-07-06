"""Servicio de calculo de parametros acusticos segun ISO 3382.

Milestone 3: Analisis de parametros acusticos.
"""

import numpy as np
import scipy.signal

from app.services.filter import filtro_octava


def suavizar_signal(
    signal: np.ndarray,
    ventana: int | str = "hilbert",
) -> np.ndarray:
    """
    Suaviza una señal para reducir fluctuaciones del ruido.

    Parameters
    ----------
    signal : np.ndarray
        Señal de entrada (típicamente una RI filtrada por banda).

    ventana : int | str
        Si es int: tamaño de la ventana para media móvil (en muestras).
        Si es "hilbert": utiliza la envolvente obtenida mediante
        la transformada de Hilbert.

    Returns
    -------
    np.ndarray
        Señal suavizada.
    """

    # Convertir la entrada a ndarray de tipo float
    signal = np.asarray(signal, dtype=float)

    # Si la señal es 2D (por ejemplo, audio estéreo),
    # convertirla a un vector 1D
    if signal.ndim == 2:
        signal = signal.flatten()

    # Verificar que la entrada sea un vector
    if signal.ndim != 1:
        raise ValueError("ri debe ser un array unidimensional o bidimensional.")

    elif signal.ndim != 1:
        raise ValueError("signal debe ser un vector 1D o matriz 2D.")
    if ventana == "hilbert":
        # Convertir la señal a tipo float para asegurar
        # compatibilidad con las operaciones numéricas.
        signal = np.asarray(signal, dtype=float)

        # Señal analítica compleja asociada a la señal real.
        analitica = scipy.signal.hilbert(signal)

        # Envolvente de amplitud calculada como el módulo
        # de la señal analítica.
        return np.abs(analitica)

    # Caso 2: suavizado mediante un filtro de media móvil.
    if isinstance(ventana, int):
        # Verificar que el tamaño de la ventana sea válido.
        if ventana < 1:
            raise ValueError(
                "El tamaño de la ventana debe ser un entero positivo.",
            )

        # Kernel de media móvil normalizado para preservar
        # el valor medio de la señal.
        kernel = np.ones(ventana, dtype=float) / ventana

        # Convolución de la señal con el kernel.
        # mode="same" garantiza que la salida tenga
        # la misma longitud que la señal de entrada.
        return np.convolve(signal, kernel, mode="same")

    # Si se llega a este punto, el parámetro 'ventana'
    # no tiene un formato admitido.
    raise ValueError(
        "ventana debe ser un entero positivo o la cadena 'hilbert'.",
    )


def integral_schroeder(ri: np.ndarray) -> np.ndarray:
    """Calcula la integral de Schroeder (Energy Decay Curve).

    Parameters
    ----------
    ri : np.ndarray
        Respuesta al impulso (array 1D).

    Returns
    -------
    np.ndarray
        Curva de decaimiento energetico (EDC), normalizada.

    References
    ----------
    .. [1] Schroeder, M. R. (1965). "New method of measuring reverberation
       time." The Journal of the Acoustical Society of America.
    """
    # Convertir la entrada a ndarray de tipo float
    ri = np.asarray(ri, dtype=float)

    # Si la señal es 2D (por ejemplo, audio estéreo),
    # convertirla a un vector 1D
    if ri.ndim == 2:
        ri = ri.flatten()

    # Verificar que la entrada sea un vector
    if ri.ndim != 1:
        raise ValueError("ri debe ser un array unidimensional o bidimensional.")

    # Energía total de la respuesta al impulso
    energia_total = np.sum(ri**2)

    # Evitar división por cero
    if energia_total == 0:
        raise ValueError("La respuesta al impulso tiene energía nula.")

    # Energía acumulada inversa (desde cada muestra hasta el final)
    energia_acumulada = np.cumsum(ri[::-1] ** 2)[::-1]

    # Curva de decaimiento energético normalizada (entre 0 y 1)
    edc = energia_acumulada / energia_total

    return edc


def regresion_lineal(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    """
    Calcula la regresion lineal por minimos cuadrados.

    Parameters
    ----------
    x : np.ndarray
        Variable independiente (tipicamente tiempo en segundos).
    y : np.ndarray
        Variable dependiente (tipicamente curva de Schroeder en dB).

    Returns
    -------
    tuple[float, float, float]
        (pendiente, ordenada_al_origen, r_cuadrado)
        pendiente en dB/s, ordenada en dB, coeficiente de determinacion.

    Raises
    ------
    ValueError
        Si los arrays tienen distinto largo o menos de 2 puntos.
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)

    if len(x) != len(y):
        raise ValueError(f"x e y deben tener el mismo largo. Got len(x)={len(x)}, len(y)={len(y)}")
    if len(x) < 2:
        raise ValueError("Se necesitan al menos 2 puntos para la regresion.")

    N = len(x)

    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x**2)

    denominador = N * sum_x2 - sum_x**2

    if denominador == 0:
        raise ValueError("Los valores de x son constantes, no se puede ajustar una recta.")

    m = (N * sum_xy - sum_x * sum_y) / denominador
    b = (sum_y - m * sum_x) / N

    y_pred = m * x + b
    y_media = np.mean(y)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y_media) ** 2)

    r_cuadrado = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0

    return float(m), float(b), float(r_cuadrado)


def calcular_parametros_acusticos(ri: np.ndarray, fs: int) -> dict[str, dict[float, float]]:
    """Calcula los parametros acusticos de una sala a partir de su RI para cada banda de octava.

    Parameters
    ----------
    ri : np.ndarray
        Respuesta al impulso (array 1D).
    fs : int
        Frecuencia de muestreo en Hz.

    Returns
    -------
    dict[str, dict[float, float]]
        Diccionario con los parametros acusticos por banda.

    References
    ----------
    .. [1] ISO 3382-1:2009. "Acoustics -- Measurement of room acoustic
       parameters -- Part 1: Performance spaces."
    """
    ri = np.asarray(ri, dtype=float)

    if ri.ndim != 1:
        raise ValueError("La respuesta al impulso debe ser un vector unidimensional.")

    if fs <= 0:
        raise ValueError("La frecuencia de muestreo debe ser mayor que cero.")

    # Bandas de octava normalizadas
    bandas = [125, 250, 500, 1000, 2000, 4000, 8000]

    parametros = {
        "EDT": {},
        "T10": {},
        "T20": {},
        "T30": {},
        "T60": {},
        "D50": {},
        "C80": {},
    }

    for fc in bandas:
        # Filtrado por banda de octava
        ri_filtrada = filtro_octava(
            signal=ri,
            fc=fc,
            fs=fs,
        )

        # Curva de Schroeder
        edc = integral_schroeder(ri_filtrada)
        eps = np.finfo(float).eps
        edc_db = 10 * np.log10(np.maximum(edc, eps))
        tiempo = np.arange(len(ri_filtrada)) / fs

        # Función auxiliar para EDT, T10, T20 y T30, para no escribir el mismo procedimiento
        # en todos los casos, simplemente toma los límites de cada parámetros y hace el cálculo.

        def calcular_rt(db_inicio: float, db_fin: float) -> float:

            indice_inicio = np.argmin(np.abs(edc_db - db_inicio))
            indice_fin = np.argmin(np.abs(edc_db - db_fin))

            if indice_fin <= indice_inicio:
                return np.nan

            pendiente, _, _ = regresion_lineal(
                tiempo[indice_inicio : indice_fin + 1],
                edc_db[indice_inicio : indice_fin + 1],
            )

            if pendiente >= 0:
                return np.nan

            return -60.0 / pendiente

        # Tiempos de reverberación
        edt = calcular_rt(0, -10)
        t10 = calcular_rt(-5, -15)
        t20 = calcular_rt(-5, -25)
        t30 = calcular_rt(-5, -35)

        # ISO 3382: normalmente se reporta T30 como T60
        t60 = t30 if not np.isnan(t30) else t20

        # Energía
        energia = ri_filtrada**2
        energia_total = np.sum(energia)

        if energia_total == 0:
            d50 = np.nan
            c80 = np.nan
        else:
            # D50
            n50 = min(int(round(0.050 * fs)), len(energia))
            energia_50 = np.sum(energia[:n50])
            d50 = 100 * energia_50 / energia_total

            # C80
            n80 = min(int(round(0.080 * fs)), len(energia))
            energia_80 = np.sum(energia[:n80])
            energia_tardia = np.sum(energia[n80:])

            c80 = np.inf if energia_tardia <= 0 else 10 * np.log10(energia_80 / energia_tardia)
        # Guardar resultados

        parametros["EDT"][fc] = float(edt)
        parametros["T10"][fc] = float(t10)
        parametros["T20"][fc] = float(t20)
        parametros["T30"][fc] = float(t30)
        parametros["T60"][fc] = float(t60)
        parametros["D50"][fc] = float(d50)
        parametros["C80"][fc] = float(c80)

    return parametros


def metodo_lundeby(
    ri: np.ndarray,
    fs: int,
) -> tuple[int, float]:
    """Estima el punto de truncamiento de la RI (metodo de Lundeby).

    Parameters
    ----------
    ri : np.ndarray
        Respuesta al impulso (array 1D).
    fs : int
        Frecuencia de muestreo en Hz.

    Returns
    -------
    tuple[int, float]
    (indice_truncamiento, nivel_ruido_dB)

    Notes
    -----
    Esta funcion es **opcional** (extra credit).

    References
    ----------
    .. [1] Lundeby, A. et al. (1995). "Uncertainties of measurements in
       room acoustics." Acta Acustica.
    """
    ri = np.asarray(ri, dtype=float)

    if ri.ndim != 1:
        raise ValueError("RI debe ser 1D.")

    if len(ri) < 10:
        return len(ri) - 1, float("nan")

    # Energía y curva de Schroeder

    energia = ri**2
    energia = np.maximum(energia, np.finfo(float).eps)

    edc = integral_schroeder(ri)
    eps = np.finfo(float).eps
    edc_db = 10 * np.log10(np.maximum(edc, eps))

    t = np.arange(len(ri)) / fs

    # Estimación inicial de ruido (últimos 10%)

    n = len(ri)
    n_ruido = max(int(0.1 * n), 10)

    ruido_db = 10 * np.log10(np.mean(energia[-n_ruido:]))

    indice_trunc = int(0.5 * n)

    m = 0.0
    b = edc_db[0]

    # Iteraciones Lundeby
    for _ in range(5):
        nivel_corte = ruido_db + 10

        idx = np.where(edc_db <= nivel_corte)[0]

        if len(idx) == 0:
            break

        indice_trunc = idx[0]

        if indice_trunc < 5:
            break

        # regresión hasta el punto de cruce
        m, b, _ = regresion_lineal(t[:indice_trunc], edc_db[:indice_trunc])

        # estimación de la curva
        fit = m * t + b

        residuo = edc_db - fit

        ruido_db = np.mean(residuo[-n_ruido:])

    # Cruce final con el nivel de ruido

    fit_final = m * t + b

    diff = fit_final - ruido_db

    cruces = np.where(diff <= 0)[0]

    if len(cruces) == 0:
        return len(ri) - 1, float(ruido_db)

    return int(cruces[0]), float(ruido_db)

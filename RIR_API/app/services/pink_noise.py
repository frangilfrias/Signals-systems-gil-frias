"""Servicio de generacion de ruido rosa.

Milestone 1: Generacion de senales.
"""

import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

# def generar_ruido_rosa(duracion: float, fs: int) -> np.ndarray:
# """Genera una senal de ruido rosa de la duracion especificada.

# El ruido rosa tiene una densidad espectral de potencia inversamente
#  proporcional a la frecuencia (1/f). Esto significa que cada octava
#  contiene la misma cantidad de energia, lo cual lo hace util para
#  mediciones acusticas.

#  Algoritmo sugerido:
#   1. Generar ruido blanco (distribucion normal) de la duracion deseada.
#  2. Aplicar la transformada de Fourier (np.fft.rfft).
#  3. Crear un vector de frecuencias correspondiente.
#  4. Dividir cada componente por sqrt(f) (omitir f=0 para evitar division por cero).
#  5. Aplicar la transformada inversa (np.fft.irfft).
#  6. Normalizar la senal resultante al rango [-1, 1].

#  Parameters
#  ----------
#  duracion : float
#      Duracion de la senal en segundos.
#  fs : int
#      Frecuencia de muestreo en Hz.

#  Returns
# -------
#  np.ndarray
#      Senal de ruido rosa normalizada, de longitud ``int(duracion * fs)``.
#  """
# raise NotImplementedError("Implementar en Milestone 1")
# Generar ruido blanco

sr_gen = 44100


def generar_ruido_rosa(duracion: float, fs: int) -> np.ndarray:

    n_muestras = int(fs * duracion)

    # Generar ruido blanco (distribucion normal) de la duracion deseada.
    ruido_blanco = np.random.randn(n_muestras)

    # Normalización de ruido blanco [-1,1] (línea auxiliar para verificar funcionalidad. Eliminar)
    ruido_blanco = ruido_blanco / np.max(np.abs(ruido_blanco))
    # Aplicar la transformada de Fourier (np.fft.rfft)
    espectro = np.fft.rfft(ruido_blanco)
    # Crear vector de frecuencias (ventajas de np.fft sobre np.linspace)
    freqs = np.fft.rfftfreq(n_muestras, d=1 / fs)
    # Espectro de ruido blanco
    espectro_ruido_blanco = espectro.copy()
    # Dividir cada componente por sqrt(f) (omitir f=0 para evitar division por cero)
    espectro[1:] /= np.sqrt(freqs[1:])

    # Aplicar la transformada inversa (np.fft.irfft)
    ruido_rosa = np.fft.irfft(espectro)

    # Normalización de ruido_rosa  [-1,1] según el algoritmo sugerido (normalización dura)
    ruido_rosa = ruido_rosa / (np.max(np.abs(ruido_rosa)))

    return ruido_rosa, freqs, espectro, espectro_ruido_blanco, ruido_blanco


# Parámetros
duracion = 30
fs = 44100
# Ejecutar función
ruido_rosa, freqs, espectro, espectro_ruido_blanco, ruido_blanco = generar_ruido_rosa(duracion, fs)

# sd.play(ruido_rosa)
# sd.wait()
# sd.play(ruido_blanco)
# sd.wait()

# Guardar como WAV
sf.write(r"C:\UNTREF\2026\PARTE PRÁCTICA\TP1\M1\RUIDO_ROSA.wav", ruido_rosa, fs)
sf.write(r"C:\UNTREF\2026\PARTE PRÁCTICA\TP1\M1\RUIDO_BLANCO.wav", ruido_blanco, fs)


fig, axes = plt.subplots(2, 1, figsize=(10, 8))

# =========================
# ESPECTRO RUIDO ROSA
# =========================

magnitud = np.abs(espectro)

magnitud_db = 20 * np.log10(magnitud + 1e-12)

axes[0].semilogx(freqs, magnitud_db)

axes[0].set_title("Espectro del ruido rosa")

axes[0].set_xlabel("Frecuencia [Hz]")

axes[0].set_ylabel("Magnitud [dB]")

axes[0].grid(True)


# =========================
# ESPECTRO RUIDO BLANCO
# =========================

magnitud_ruido_blanco = np.abs(espectro_ruido_blanco)

magnitud_ruido_blanco_db = 20 * np.log10(magnitud_ruido_blanco + 1e-12)

axes[1].semilogx(freqs, magnitud_ruido_blanco_db)

axes[1].set_title("Espectro del ruido blanco")

axes[1].set_xlabel("Frecuencia [Hz]")

axes[1].set_ylabel("Magnitud [dB]")

axes[1].grid(True)


plt.tight_layout()

plt.show()
# sf.write("/tmp/ruido_blanco.wav", ruido, sr_gen)
# print(f"Ruido blanco generado: {duracion} s, pico = {np.max(np.abs(ruido)):.2f}")

# Visualizar
fig_ruido_blanco, axes_ruido = plt.subplots(2, 1, figsize=(10, 5))

# Forma de onda (primeros 50 ms)
muestras_r = int(0.05 * sr_gen)
t_ruido = np.arange(muestras_r) / sr_gen * 1000
axes_ruido[0].plot(t_ruido, ruido_blanco[:muestras_r], "gray", linewidth=0.5)
axes_ruido[0].set_title("Ruido blanco - forma de onda (50 ms)")
axes_ruido[0].set_xlabel("Tiempo (ms)")
axes_ruido[0].set_ylabel("Amplitud")
axes_ruido[0].grid(True, alpha=0.3)

# Histograma (distribucion gaussiana)
axes_ruido[1].hist(ruido_blanco, bins=100, density=True, alpha=0.7, color="steelblue")
axes_ruido[1].set_title("Distribucion del ruido (debe ser gaussiana)")
axes_ruido[1].set_xlabel("Amplitud")
axes_ruido[1].set_ylabel("Densidad")
axes_ruido[1].grid(True, alpha=0.3)

plt.tight_layout()
# plt.gca()
plt.show()

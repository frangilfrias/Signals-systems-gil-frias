"""Tests para los endpoints de la API (Milestone 3)."""

from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    """Verifica que el endpoint /health responda correctamente."""

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


def test_pink_noise():
    """
    Verifica que el endpoint genere un archivo WAV de ruido rosa.
    """

    response = client.post(
        "/api/v1/signals/pink-noise",
        params={
            "duracion": 1.0,
            "fs": 44100,
        },
    )

    assert response.status_code == 200

    assert response.headers["content-type"] == "audio/wav"

    assert "pink_noise.wav" in response.headers["content-disposition"]

    assert len(response.content) > 0


def test_sine_sweep():
    """
    Verifica que el endpoint genere un archivo WAV con un sine sweep.
    """

    response = client.post(
        "/api/v1/signals/sine-sweep",
        params={
            "f1": 20,
            "f2": 20000,
            "duracion": 5.0,
            "fs": 44100,
        },
    )

    assert response.status_code == 200

    assert response.headers["content-type"] == "audio/wav"

    assert "sine_sweep.wav" in response.headers["content-disposition"]

    # Verifica que realmente sea un archivo WAV
    assert response.content[:4] == b"RIFF"


def test_synthetic_ir():
    """
    Verifica que el endpoint genere una respuesta al impulso sintética.
    """

    response = client.post(
        "/api/v1/signals/synthetic-ir",
        params={
            "fs": 44100,
            "duracion": 3.0,
        },
    )

    assert response.status_code == 200

    assert response.headers["content-type"] == "audio/wav"

    assert "synthetic_ir.wav" in response.headers["content-disposition"]

    # Verifica que el archivo generado sea un WAV válido
    assert response.content[:4] == b"RIFF"


def test_filter_band():
    """
    Verifica que el endpoint filtre un archivo de audio
    y devuelva un WAV válido.
    """

    audio_path = Path(__file__).parent / "data_tests" / "grabacion.wav"

    with open(audio_path, "rb") as audio:
        response = client.post(
            "/api/v1/filters/band",
            params={
                "fc": 1000,
                "orden": 4,
            },
            files={
                "archivo": ("grabacion.wav", audio, "audio/wav"),
            },
        )

    assert response.status_code == 200

    assert response.headers["content-type"] == "audio/wav"

    assert "band_1000Hz.wav" in response.headers["content-disposition"]

    assert response.content[:4] == b"RIFF"


def test_frequencies():
    """
    Verifica que el endpoint devuelva las frecuencias
    centrales soportadas.
    """

    response = client.get("/api/v1/filters/frequencies")

    assert response.status_code == 200

    data = response.json()

    assert "frequencies_hz" in data

    assert data["frequencies_hz"] == [
        31.5,
        63,
        125,
        250,
        500,
        1000,
        2000,
        4000,
        8000,
        16000,
    ]


def test_acoustic_parameters():
    """
    Verifica que el endpoint calcule correctamente
    los parámetros acústicos.
    """

    audio_path = Path(__file__).parent / "data_tests" / "grabacion.wav"

    with open(audio_path, "rb") as audio:
        response = client.post(
            "/api/v1/acoustics/parameters",
            files={
                "file": ("grabacion.wav", audio, "audio/wav"),
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "sample_rate" in data
    assert "parameters" in data

    parametros = data["parameters"]

    assert "EDT" in parametros
    assert "T10" in parametros
    assert "T20" in parametros
    assert "T30" in parametros
    assert "T60" in parametros
    assert "D50" in parametros
    assert "C80" in parametros


def test_acoustic_parameters_by_bands():
    """
    Verifica que el endpoint devuelva los parámetros
    acústicos agrupados por banda.
    """

    audio_path = Path(__file__).parent / "data_tests" / "grabacion.wav"

    with open(audio_path, "rb") as audio:
        response = client.post(
            "/api/v1/acoustics/by-bands",
            files={
                "file": ("grabacion.wav", audio, "audio/wav"),
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "sample_rate" in data
    assert "bands" in data

    bands = data["bands"]

    # Verificar que exista al menos una banda
    assert len(bands) > 0

    # Verificar una banda conocida
    banda_1000 = bands["1000"]

    assert "EDT" in banda_1000
    assert "T10" in banda_1000
    assert "T20" in banda_1000
    assert "T30" in banda_1000
    assert "T60" in banda_1000
    assert "D50" in banda_1000
    assert "C80" in banda_1000


def test_analysis_impulse_response():
    """
    Verifica que el endpoint realice un análisis completo
    de una respuesta al impulso.
    """

    audio_path = Path(__file__).parent / "data_tests" / "grabacion.wav"

    with open(audio_path, "rb") as audio:
        response = client.post(
            "/api/v1/analysis/impulse-response",
            files={
                "file": ("grabacion.wav", audio, "audio/wav"),
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "sample_rate" in data
    assert "samples" in data
    assert "duration" in data
    assert "schroeder_points" in data
    assert "schroeder_preview" in data
    assert "acoustic_parameters" in data

    assert isinstance(data["schroeder_points"], int)
    assert data["schroeder_points"] > 0

    assert isinstance(data["schroeder_preview"], list)
    assert len(data["schroeder_preview"]) > 0

    parametros = data["acoustic_parameters"]

    assert "EDT" in parametros
    assert "T10" in parametros
    assert "T20" in parametros
    assert "T30" in parametros
    assert "T60" in parametros
    assert "D50" in parametros
    assert "C80" in parametros


def test_schroeder():
    """
    Verifica que el endpoint calcule la integral de Schroeder.
    """

    audio_path = Path(__file__).parent / "data_tests" / "grabacion.wav"

    with open(audio_path, "rb") as audio:
        response = client.post(
            "/api/v1/utils/schroeder",
            files={
                "file": ("grabacion.wav", audio, "audio/wav"),
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "sample_rate" in data
    assert "samples" in data
    assert "schroeder_points" in data
    assert "schroeder_preview" in data

    assert data["schroeder_points"] > 0
    assert isinstance(data["schroeder_preview"], list)
    assert len(data["schroeder_preview"]) > 0


def test_smoothing():
    """
    Verifica que el endpoint suavice correctamente
    una respuesta al impulso.
    """

    audio_path = Path(__file__).parent / "data_tests" / "grabacion.wav"

    with open(audio_path, "rb") as audio:
        response = client.post(
            "/api/v1/utils/smoothing",
            params={
                "method": "hilbert",
            },
            files={
                "file": ("grabacion.wav", audio, "audio/wav"),
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["method"] == "hilbert"
    assert "num_samples" in data
    assert "signal_preview" in data

    assert isinstance(data["signal_preview"], list)
    assert len(data["signal_preview"]) > 0
    assert data["num_samples"] > 0


def test_log_scale():
    """
    Verifica que el endpoint convierta una señal
    a escala logarítmica (dB).
    """

    audio_path = Path(__file__).parent / "data_tests" / "grabacion.wav"

    with open(audio_path, "rb") as audio:
        response = client.post(
            "/api/v1/utils/log-scale",
            files={
                "file": ("grabacion.wav", audio, "audio/wav"),
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "num_samples" in data
    assert "min_db" in data
    assert "max_db" in data
    assert "file_path" in data
    assert "signal_db_preview" in data

    assert isinstance(data["signal_db_preview"], list)
    assert len(data["signal_db_preview"]) > 0

    assert isinstance(data["min_db"], (int, float))
    assert isinstance(data["max_db"], (int, float))

    assert data["max_db"] >= data["min_db"]

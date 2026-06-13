import numpy as np

from app.services.signal_utils import a_escala_log


class TestAEscalaLog:
    def test_maximo_es_0_db(self):
        signal = np.array([1.0, 0.5, 0.25])
        resultado = a_escala_log(signal)
        assert np.isclose(np.max(resultado), 0.0, atol=1e-6)

    def test_amplitud_mitad_da_menos6_db(self):
        signal = np.array([1.0, 0.5])
        resultado = a_escala_log(signal)
        assert np.isclose(resultado[1], -6.0206, atol=0.01)

    def test_output_mismo_shape_que_input(self):
        signal = np.array([1.0, 0.5, 0.25, 0.1])
        resultado = a_escala_log(signal)
        assert resultado.shape == signal.shape

    def test_no_hay_inf(self):
        signal = np.array([1.0, 0.5, 0.0, 0.25])
        resultado = a_escala_log(signal)
        assert not np.any(np.isinf(resultado))

    def test_piso_de_ruido(self):
        signal = np.array([1.0, 1e-10])
        resultado = a_escala_log(signal)
        assert np.all(resultado >= -120.0)

    def test_senal_con_negativos(self):
        signal = np.array([1.0, -1.0, 0.5, -0.5])
        resultado = a_escala_log(signal)
        assert np.isclose(np.max(resultado), 0.0, atol=1e-6)

    def test_senal_silencio_total(self):
        signal = np.zeros(10)
        resultado = a_escala_log(signal)
        assert not np.any(np.isinf(resultado))

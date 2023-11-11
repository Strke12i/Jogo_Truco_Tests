from truco.pontos import MANILHA, CARTAS_VALORES, ENVIDO
import pytest

@pytest.mark.parametrize("carta, valor", [
    ("1 de ESPADAS", 52),
    ("1 de BASTOS", 50),
    ("7 de ESPADAS", 42),
    ("7 de OUROS", 40),
])
def test_manilha(carta, valor):
    assert MANILHA[carta] == valor

@pytest.mark.parametrize("carta, valor", [
    ("3", 24),
    ("2", 16),
    ("1", 12),
    ("12", 8),
    ("11", 7),
    ("10", 6),
    ("7", 4),
    ("6", 3),
    ("5", 2),
    ("4", 1),
])
def test_cartas_valores(carta, valor):
    assert CARTAS_VALORES[carta] == valor

@pytest.mark.parametrize("carta, valor", [
    ("3", 3),
    ("2", 2),
    ("1", 1),
    ("12", 0),
    ("11", 0),
    ("10", 0),
    ("7", 7),
    ("6", 6),
    ("5", 5),
    ("4", 4),
])
def test_envido(carta, valor):
    assert ENVIDO[carta] == valor

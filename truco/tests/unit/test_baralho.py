from truco.baralho import Baralho
from truco.carta import Carta
import pytest

@pytest.fixture
def baralho():
    return Baralho()

def test_criar_baralho(baralho):
    assert len(baralho.cartas) == 40
    for i in baralho.cartas:
        assert isinstance(i, Carta)
        assert i.numero != 8 and i.numero != 9
        assert i.naipe == "ESPADAS" or i.naipe == "OUROS" or i.naipe == "COPAS" or i.naipe == "BASTOS"

def test_embaralhar(baralho):
    try:
        baralho.embaralhar()
    except:
        assert False

def test_retirar_carta(baralho):
    count = 40
    for i in range(0,10):
        baralho.retirar_carta()
        assert len(baralho.cartas) == count - 1
        count -= 1
    
    assert len(baralho.cartas) == 30

def test_resetar(baralho):
    try:
        baralho.resetar()
        assert len(baralho.cartas) == 0
        assert len(baralho.manilhas) == 0
        assert len(baralho.vira) == 0
    except:
        assert False

def test_printar_baralho(baralho, capsys):
    try:
        baralho.printar_baralho()
        captured = capsys.readouterr()
        assert captured.out != ""
    except:
        assert False

    
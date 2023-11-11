try:
    from sklearn.neighbors import NearestNeighbors
    import sklearn.neighbors._unsupervised
    import pandas as pd
    import warnings
except ImportError:
    assert False

from truco.dados import Dados
from truco.cbr import Cbr

import pytest

@pytest.fixture
def cbr():
    return Cbr()

@pytest.fixture
def dados():
    return Dados()

def test_vizinhos_proximos(cbr, dados):
    assert type(cbr.vizinhos_proximos(None)) == sklearn.neighbors._unsupervised.NearestNeighbors

def test_cbr(cbr, dados):
    assert cbr.indice == 0
    assert type(cbr.dados) == Dados
    assert type(cbr.dataset) == pd.core.frame.DataFrame
    assert type(cbr.nbrs) == sklearn.neighbors._unsupervised.NearestNeighbors
    
def test_carregar_dataset(cbr, dados):
    df = cbr.carregar_dataset()
    assert type(df) == pd.core.frame.DataFrame
    assert df.index.name == "idMao"
    assert "ESPADAS" not in df.values
    assert "OURO" not in df.values
    assert "BASTOS" not in df.values
    assert "COPAS" not in df.values
    
def test_jogar_carta(cbr):
    assert cbr.jogar_carta(1, [1, 2, 3]) == 0
    assert cbr.jogar_carta(1, [1, 2, 3, 4, 5]) == 0
    assert cbr.jogar_carta(2, [1, 2, 3, 4, 5]) == 1
    assert cbr.jogar_carta(3, [1, 2, 3, 4, 5]) == 4
    
def test_truco(cbr):
    assert cbr.truco(1, 2, 3) == 2
    assert cbr.truco(2, 1, 100) == 2
    assert cbr.truco(2, 2, 3) == 2
    assert cbr.truco(2, 1, 0) == 0
    assert cbr.truco(1, 2, 0) == 0

def test_envido(cbr):
    assert cbr.envido(0, 2, 6, True) == 8
    assert cbr.envido(0, 2, 6, False) == 6
    assert cbr.envido(6, 1, 0, True) == 1
    assert cbr.envido(6, 1, -3, True) == 1
    assert cbr.envido(6, 1, 100, True) == 1
    assert cbr.envido(7, 1, 0, False) == 0
    assert cbr.envido(7, 1, 100, False) == 1
    
    
    
    
    
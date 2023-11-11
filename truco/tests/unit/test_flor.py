from truco.flor import Flor
from truco.jogador import Jogador
from truco.bot import Bot
from truco.interface import Interface

import pytest

@pytest.fixture
def flor():
    return Flor() 

@pytest.fixture
def jogador1():
    return Jogador("Jogador 1")

@pytest.fixture
def jogador2():
    return Bot("Jogador 2")

@pytest.fixture
def interface():
    return Interface()

def test_flor(flor):
    assert flor.valor_flor == 3
    assert flor.quem_pediu_flor == 0
    assert flor.quem_pediu_contraflor == 0
    assert flor.quem_pediu_contraflor_resto == 0
    assert flor.quem_venceu_flor == 0
    assert flor.estado_atual == ""
    
def test_contraflor(flor, jogador1, jogador2):
    jogador1.envido = 3
    jogador2.envido = 2
    
    try:
        flor.contraflor(1, jogador1, jogador2)
    except:
        assert False
        
    assert flor.valor_flor == 6
    assert flor.quem_venceu_flor == 1
    assert jogador1.pontos == 6
    
    jogador2.envido = 3
    try:
        flor.contraflor(1, jogador1, jogador2)
    except:
        assert False
        
    assert flor.valor_flor == 6
    assert flor.quem_venceu_flor == 1
    assert jogador1.pontos == 12
    
    jogador2.envido = 4
    try:
        flor.contraflor(1, jogador1, jogador2)
    except:
        assert False
        
    assert flor.valor_flor == 6
    assert flor.quem_venceu_flor == 2
    assert jogador1.pontos == 12
    assert jogador2.pontos == 6
    
def test_contraflor_resto(flor, jogador1, jogador2):
    jogador1.envido = 3
    jogador2.envido = 2
    flor.valor_flor = 1
    
    try:    
        flor.contraflor_resto(1, jogador1, jogador2)
    except:
        assert False
        
    assert jogador1.pontos == 1
    assert flor.quem_venceu_flor == 1
    
    jogador2.envido = 4
    try:
        flor.contraflor_resto(2, jogador1, jogador2)
    except:
        assert False
    
    assert jogador2.pontos == 1
    assert flor.quem_venceu_flor == 2
    
def test_decisao_jogador(flor, monkeypatch):
    r = iter([10000, 0])
    try:
        monkeypatch.setattr('builtins.input', lambda _: next(r))
        assert flor.decisao_jogador() == False
    except:
        assert False
        
    monkeypatch.setattr('builtins.input', lambda _: 1)
    assert flor.decisao_jogador() == True
    
def test_resetar_flor(flor):
    try:
        flor.resetar_flor()
    except:
        assert False

    assert flor.valor_flor == 3
    assert flor.quem_pediu_flor == 0
    assert flor.quem_pediu_contraflor == 0
    assert flor.quem_pediu_contraflor_resto == 0
    assert flor.quem_venceu_flor == 0
    assert flor.estado_atual == ""
    


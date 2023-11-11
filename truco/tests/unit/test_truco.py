from truco.truco import Truco
from truco.cbr import Cbr
from truco.jogador import Jogador
from truco.bot import Bot

import pytest

@pytest.fixture
def truco():
    return Truco()

@pytest.fixture
def cbr():
    return Cbr()

@pytest.fixture
def jogador1():
    return Jogador("Jogador 1")

@pytest.fixture
def jogador2():
    return Bot("Jogador 2")

def test_truco(truco):
    assert truco.valor_aposta == 1
    assert truco.jogador_bloqueado == 0
    assert truco.jogador_pediu == 0
    assert truco.jogador_retruco == 0
    assert truco.jogador_vale_quatro == 0
    assert truco.jogador_fugiu == 0
    assert truco.estado_atual == ""
    
def test_inverter_jogador_bloqueado(truco):
    truco.jogador_bloqueado = 1
    try:
        truco.inverter_jogador_bloqueado()
    except:
        assert False
    assert truco.jogador_bloqueado == 2
    
    truco.jogador_bloqueado = 2
    try:
        truco.inverter_jogador_bloqueado()
    except:
        assert False
    assert truco.jogador_bloqueado == 1
    
def test_inicializar_jogador_bloqueado(truco):
    try:
        truco.inicializar_jogador_bloqueado(1)
    except:
        assert False
        
    assert truco.jogador_bloqueado == 1
    
def test_retornar_valor_aposta(truco):
    truco.valor_aposta = 2
    assert truco.retornar_valor_aposta() == 2
    
def test_retornar_quem_fugiu(truco):
    try:
        truco.retornar_quem_fugiu() == 1
        assert False
    except:
        assert True
        
def test_resetar(truco):
    try:
        truco.resetar()
    except:
        assert False
        
    assert truco.valor_aposta == 1
    assert truco.jogador_bloqueado == 0
    assert truco.jogador_pediu == 0
    assert truco.jogador_retruco == 0
    assert truco.jogador_vale_quatro == 0
    assert truco.jogador_fugiu == 0
    assert truco.estado_atual == ""
    
def test_pedir_vale_quatro(truco, cbr, jogador1, jogador2, monkeypatch, capsys):
    truco.jogador_bloqueado = 1
    try:
        assert truco.pedir_vale_quatro(cbr, 1, jogador1, jogador2) == False
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Vale 4\n"
    assert truco.valor_aposta == 4
    assert truco.jogador_bloqueado == 1
    assert jogador2.avaliar_truco(cbr, truco.estado_atual, 1) == 0
    assert jogador1.pontos == 3
    
    try:
        monkeypatch.setattr('builtins.input', lambda _: 0)
        assert truco.pedir_vale_quatro(cbr, 2, jogador1, jogador2) == False
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Vale 4\n"
    assert truco.valor_aposta == 4
    assert truco.jogador_bloqueado == 2
    assert jogador2.pontos == 3
    
    try:
        monkeypatch.setattr('builtins.input', lambda _: 1)
        assert truco.pedir_vale_quatro(cbr, 2, jogador1, jogador2) == True
    except:
        assert False
        
    out, err = capsys.readouterr()
    assert out == "Vale 4\nJogador 2 aceitou o pedido.\n"
    assert jogador1.pediu_truco == True
    assert jogador2.pediu_truco == True
    
def test_pedir_retruco(truco, cbr, jogador1, jogador2, monkeypatch, capsys):
    try:
        assert truco.pedir_retruco(cbr, 1, jogador1, jogador2) == False
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Retruco\n"
    assert truco.jogador_bloqueado == 1
    assert jogador2.avaliar_truco(cbr, truco.estado_atual, 1) == 0
    assert jogador1.pontos == 2
    
    try:
        monkeypatch.setattr('builtins.input', lambda _: 0)
        assert truco.pedir_retruco(cbr, 2, jogador1, jogador2) == False
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Retruco\n"
    assert truco.jogador_bloqueado == 2
    assert jogador2.pontos == 2
    
    try:
        monkeypatch.setattr('builtins.input', lambda _: 1)
        assert truco.pedir_retruco(cbr, 2, jogador1, jogador2) == True
    except:
        assert False
        
    out, err = capsys.readouterr()
    assert out == "Retruco\nJogador 2 aceitou o pedido.\n"
    assert truco.jogador_bloqueado == 2
    
    try:
        monkeypatch.setattr('builtins.input', lambda _: 2)
        assert truco.pedir_retruco(cbr, 2, jogador1, jogador2) == False
    except:
        assert False
        
    out, err = capsys.readouterr()
    assert out == "Retruco\nJogador 2 pediu Retruco.\nVale 4\n"
    assert truco.jogador_bloqueado == 1
    
def test_pedir_truco(truco, cbr, jogador1, jogador2, monkeypatch, capsys):
    try:
        assert truco.pedir_truco(cbr, 1, jogador1, jogador2) == False
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Truco\n"
    assert truco.jogador_bloqueado == 1
    assert jogador2.avaliar_truco(cbr, truco.estado_atual, 1) == 0
    assert jogador1.pontos == 1
    
    try:
        monkeypatch.setattr('builtins.input', lambda _: 0)
        assert truco.pedir_truco(cbr, 2, jogador1, jogador2) == False
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Truco\n"
    assert truco.jogador_bloqueado == 2
    assert jogador2.pontos == 1
    
    try:
        monkeypatch.setattr('builtins.input', lambda _: 1)
        assert truco.pedir_truco(cbr, 2, jogador1, jogador2) == True
    except:
        assert False
        
    out, err = capsys.readouterr()
    assert out == "Truco\nJogador 2 aceitou o pedido.\n"
    assert truco.jogador_bloqueado == 2
    
    
def test_controlador_truco(truco, cbr, jogador1, jogador2, capsys, monkeypatch):
    try:
        truco.controlador_truco(cbr, None, 1, jogador1, jogador2)
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Truco\n"
    assert truco.jogador_bloqueado == 1
    assert jogador2.avaliar_truco(cbr, truco.estado_atual, 1) == 0
    assert jogador1.pontos == 1
    
    try:
        monkeypatch.setattr('builtins.input', lambda _: 0)
        truco.controlador_truco(cbr, None, 2, jogador1, jogador2)
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Retruco\n"
    assert truco.jogador_bloqueado == 2
    assert jogador2.pontos == 2
    
    try:
        monkeypatch.setattr('builtins.input', lambda _: 1)
        truco.controlador_truco(cbr, None, 2, jogador1, jogador2)
    except:
        assert False
        
    out, err = capsys.readouterr()
    assert truco.jogador_bloqueado == 2
    
    
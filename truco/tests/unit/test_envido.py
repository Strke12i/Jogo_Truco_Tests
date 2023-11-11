from truco.envido import Envido
from truco.cbr import Cbr
from truco.dados import Dados
from truco.interface import Interface
from truco.jogador import Jogador
from truco.bot import Bot

import pytest

@pytest.fixture
def envido():
    return Envido()

@pytest.fixture
def cbr():
    return Cbr()

@pytest.fixture
def dados():
    return Dados()

@pytest.fixture
def jogador1():
    return Jogador("Jogador 1")

@pytest.fixture
def jogador2():
    return Bot("Jogador 2")

@pytest.fixture
def interface():
    return Interface()

def test_envido(envido):
    assert envido.valor_envido == 2
    assert envido.estado_atual == 0
    assert envido.jogador_pediu_envido == 0
    assert envido.quem_real_envido == 0
    assert envido.quem_falta_envido == 0
    assert envido.quem_fugiu == 0
    assert envido.quem_venceu_envido == 0
    assert envido.jogador_bloqueado == 0
    assert envido.jogador1_pontos == 0
    assert envido.jogador2_pontos == 0
    
def test_inverter_jogador_bloqueado(envido):
    envido.jogador_bloqueado = 1
    try:
        envido.inverter_jogador_bloqueado()
        assert envido.jogador_bloqueado == 2
    except:
        assert False
        
    envido.jogador_bloqueado = 0
    try:
        envido.inverter_jogador_bloqueado()
        assert envido.jogador_bloqueado == 1
    except:
        assert False
        
def test_inicializar_jogador_bloqueado(envido):
    try:
        envido.inicializar_jogador_bloqueado(1)
        assert envido.jogador_bloqueado == 1
    except:
        assert False
        
    try:
        envido.inicializar_jogador_bloqueado("A")
        assert envido.jogador_bloqueado == "A"
    except:
        assert False
        
def test_definir_pontos_jogadores(envido, jogador1, jogador2):
    jogador1.envido = 2
    jogador2.envido = 3
    try:
        envido.definir_pontos_jogadores(jogador1, jogador2)
        assert envido.jogador1_pontos == 2
        assert envido.jogador2_pontos == 3
    except:
        assert False
    

def test_avaliar_vencedor_envido(envido, jogador1, jogador2):
    envido.jogador1_pontos = 2
    envido.jogador2_pontos = 1
    envido.valor_envido = 100
    
    try:
        envido.avaliar_vencedor_envido(1, jogador1, jogador2)
    except:
        assert False
        
    assert jogador1.pontos == 100
    assert envido.quem_venceu_envido == 1
    
    envido.jogador2_pontos = 2
    try:
        envido.avaliar_vencedor_envido(1, jogador1, jogador2)
    except:
        assert False
        
    assert jogador1.pontos == 200
    assert envido.quem_venceu_envido == 1
    
    envido.jogador2_pontos = 3
    try:
        envido.avaliar_vencedor_envido(1, jogador1, jogador2)
    except:
        assert False
        
    assert jogador2.pontos == 100
    assert envido.quem_venceu_envido == 2
    
def test_avaliar_vencedor_falta_envido(envido, jogador1, jogador2, capsys):
    envido.jogador1_pontos = 2
    envido.jogador1_pontos = 1
    envido.valor_envido = 100
    
    try:
        envido.avaliar_vencedor_falta_envido(1,jogador1, jogador2)
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert jogador1.pontos == 100
    assert envido.quem_venceu_envido == 1
    assert out == "3\n"
    
    envido.jogador2_pontos = 3
    try:
        envido.avaliar_vencedor_falta_envido(1,jogador1, jogador2)
    except:
        assert False
        
    out, err = capsys.readouterr()
    assert jogador2.pontos == 100
    assert envido.quem_venceu_envido == 2
    assert out == "4\n"
    
def test_falta_envido(envido, cbr, jogador1, jogador2, monkeypatch, capsys):
    try:
       assert envido.falta_envido(cbr, 1,  jogador1, jogador2) == False
    except:
        assert False
        
    out, err = capsys.readouterr()
    assert out == "1\nJogador pediu Falta Envido!\nFugiu do falta envido!\n"
    assert envido.estado_atual == 8
    assert envido.valor_envido == 12
    assert envido.jogador_pediu_envido == 1
    assert jogador2.avaliar_envido(cbr, 8, 1, 0) == 0
    assert jogador1.pontos == 5
    assert envido.quem_fugiu == 2
    
    try:
        jogador2.envido = 10
        envido.falta_envido(cbr, 1,  jogador1, jogador2)
    except:
        assert False
        
    out, err = capsys.readouterr()
    assert out == "1\nJogador pediu Falta Envido!\nAceitou Falta envido!\n3\n"
    assert jogador2.avaliar_envido(cbr, 8, 1, 1) == 1
    assert jogador1.pontos == 17
    assert envido.quem_venceu_envido == 1
    
    try:
        jogador1.pontos = 1
        jogador2.pontos = 0
        monkeypatch.setattr('builtins.input', lambda x: 0)
        envido.falta_envido(cbr, 2,  jogador1, jogador2)
    except:
        assert False
        
    out, err = capsys.readouterr()
    assert out == "2\nJogador pediu Falta Envido!\nFugiu do falta envido!\n"
    assert envido.estado_atual == 8
    assert envido.valor_envido == 11
    assert envido.jogador_pediu_envido == 2
    assert jogador2.pontos == 5
    assert envido.quem_fugiu == 1
    
    try:
        jogador1.pontos = 1
        jogador2.pontos = 0
        monkeypatch.setattr('builtins.input', lambda x: 1)
        envido.falta_envido(cbr, 2,  jogador1, jogador2)
    except:
        assert False
        
    out, err = capsys.readouterr()
    assert out == "2\nJogador pediu Falta Envido!\nAceitou Falta envido!\n3\n"
    assert envido.estado_atual == 8
    assert envido.valor_envido == 11
    assert envido.jogador_pediu_envido == 2

def test_real_envido(envido, cbr, jogador1, jogador2, monkeypatch, capsys):
    try:
        envido.real_envido(cbr, 1,  jogador1, jogador2)
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Jogador pediu Real Envido\nFugiu do Real Envido!\n"
    assert envido.estado_atual == 7
    assert envido.valor_envido == 5
    assert jogador2.avaliar_envido(cbr, 7, 1, 0) == 0
    assert envido.quem_fugiu == 2
    assert jogador1.pontos == 2
    
    try:
        jogador2.envido = 10
        envido.real_envido(cbr, 1,  jogador1, jogador2)
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Jogador pediu Real Envido\nJogador aceitou Real envido!\n"
    assert envido.estado_atual == 7
    assert envido.valor_envido == 5
    assert jogador2.avaliar_envido(cbr, 7, 1, 1) == 1
    
    try:
        jogador1.pontos = 1
        jogador2.pontos = 0
        monkeypatch.setattr('builtins.input', lambda x: 0)
        envido.real_envido(cbr, 2,  jogador1, jogador2)
    except:
        assert False
        
    out, err = capsys.readouterr()
    assert out == "Jogador pediu Real Envido\nFugiu do Real Envido!\n"
    assert jogador2.pontos == 2
    assert envido.quem_fugiu == 1
    
    try:
        jogador1.pontos = 1
        jogador2.pontos = 0
        monkeypatch.setattr('builtins.input', lambda x: 1)
        envido.real_envido(cbr, 2,  jogador1, jogador2)
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Jogador pediu Real Envido\nJogador aceitou Real envido!\n"
    
    try:
        jogador1.pontos = 1
        jogador2.pontos = 0
        r = iter([2, 0])
        monkeypatch.setattr('builtins.input', lambda x: next(r))
        envido.jogador_bloqueado = 1
        envido.real_envido(cbr, 2,  jogador1, jogador2)
    except:
        assert False
        
    out, err = capsys.readouterr()
    print(out)
    assert out == "Jogador pediu Real Envido\n2\nJogador pediu Falta Envido!\nFugiu do falta envido!\n"
    assert envido.jogador_bloqueado == 2

def test_envido(envido, cbr, jogador1, jogador2, monkeypatch, capsys):
    try:
        envido.envido(cbr, 1,  jogador1, jogador2)    
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Jogador pediu Envido!\nJogador aceitou envido!\n"
    assert envido.jogador_pediu_envido == 1
    assert envido.estado_atual == 6
    assert jogador2.avaliar_envido(cbr, 6, 1, 0) == 1
    
    try:
        monkeypatch.setattr('builtins.input', lambda x: 0)
        envido.envido(cbr, 2,  jogador1, jogador2)
    except:
        assert False
    
    out, err = capsys.readouterr()
    assert out == "Jogador pediu Envido!\nfugiu\n"
    assert jogador2.pontos == 1
    assert envido.quem_fugiu == 1
    
    try:
        monkeypatch.setattr('builtins.input', lambda x: 1)
        envido.envido(cbr, 2,  jogador1, jogador2)
    except:
        assert False
        
    out, err = capsys.readouterr()
    assert out == "Jogador pediu Envido!\nJogador aceitou envido!\n"   
     
    try:
        envido.jogador_bloqueado = 1
        monkeypatch.setattr('builtins.input', lambda x: 2)
        envido.envido(cbr, 2,  jogador1, jogador2)
    except:
        assert False
        
    out, err = capsys.readouterr()
    assert out == "Jogador pediu Envido!\nJogador pediu Real Envido\n1\nJogador pediu Falta Envido!\nFugiu do falta envido!\n"
    assert envido.jogador_bloqueado == 1
    
    try:
        envido.jogador_bloqueado = 1
        r = iter([3, 0])
        monkeypatch.setattr('builtins.input', lambda x: next(r))
        envido.envido(cbr, 2,  jogador1, jogador2)
    except:
        assert False
        
    out, err = capsys.readouterr()
    print(out)
    assert out == "Jogador pediu Envido!\n2\nJogador pediu Falta Envido!\nFugiu do falta envido!\n"
    assert envido.jogador_bloqueado == 2
    

def test_controlador_envido(envido, cbr, dados, jogador1, jogador2, interface, capsys):
    envido.estado_atual = 1
    assert envido.controlador_envido(cbr, dados, 2, 1, jogador1, jogador2, interface) == None
    
    envido.estado_atual = 0
    envido.jogador_bloqueado = 1
    assert envido.controlador_envido(cbr, dados, 2, 1, jogador1, jogador2, interface) == None
    
    try:
        jogador1.envido = 2
        jogador2.envido = 3
        envido.controlador_envido(cbr, dados, 1, 2, jogador1, jogador2, interface)
    except:
        assert False
    
    assert envido.jogador_bloqueado == 2
    assert envido.jogador1_pontos == 2
    assert envido.jogador2_pontos == 3
    
    try:
        envido.controlador_envido(cbr, dados, 6, 1, jogador1, jogador2, interface)
    except:
        assert False
        
    try:
        envido.controlador_envido(cbr, dados, 7, 1, jogador1, jogador2, interface)
    except:
        assert False
    
    try:
        envido.controlador_envido(cbr, dados, 8, 1, jogador1, jogador2, interface)
    except:
        assert False

    
    
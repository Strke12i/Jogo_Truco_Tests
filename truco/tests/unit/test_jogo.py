try:
    import random
except ImportError:
    print("Erro ao importar random")
    assert False
    
from truco.jogo import Jogo
from truco.jogador import Jogador
from truco.bot import Bot
from truco.baralho import Baralho
from truco.carta import Carta
from truco.interface import Interface

import pytest

@pytest.fixture
def jogo():
    return Jogo()

@pytest.fixture
def jogador1():
    return Jogador("Jogador 1")

@pytest.fixture
def jogador2():
    return Bot("Jogador 2")

@pytest.fixture
def baralho():
    return Baralho()

@pytest.fixture
def interface():
    return Interface()

def test_jogo(jogo):
    assert jogo.rodadas == []
    assert jogo.trucoPontos == 1
    
def test_criar_jogador(jogo, baralho):
    jogador = jogo.criar_jogador("Jogador 1", baralho)
    assert jogador.nome == "Jogador 1"
    
    try:
        jogo.criar_jogador(baralho)
        assert False
    except:
        assert True
     
def test_criar_bot(jogo, baralho):
    bot = jogo.criar_bot("Jogador 2", baralho)
    assert bot.nome == "Jogador 2"
    
    try:
        jogo.criar_bot(baralho)
        assert False
    except:
        assert True
        
def test_verificar_carta_Vencedora(jogo):
    Carta1 = Carta("1", "ESPADAS")
    Carta2 = Carta("7", "OUROS")
    assert jogo.verificar_carta_vencedora(Carta1, Carta2) == Carta1
    
    Carta1 = Carta("7", "ESPADAS")
    Carta2 = Carta("1", "BASTOS")
    assert jogo.verificar_carta_vencedora(Carta1, Carta2) == Carta2
    
    Carta1 = Carta("7", "ESPADAS")
    Carta2 = Carta("3", "BASTOS")
    assert jogo.verificar_carta_vencedora(Carta1, Carta2) == Carta1
    
    Carta1 = Carta("2", "COPAS")
    Carta2 = Carta("7", "ESPADAS")
    assert jogo.verificar_carta_vencedora(Carta1, Carta2) == Carta2
    
    Carta1 = Carta("3", "OUROS")
    Carta2 = Carta("2", "COPAS")
    assert jogo.verificar_carta_vencedora(Carta1, Carta2) == Carta1
    
    Carta1 = Carta("5", "OUROS")
    Carta2 = Carta("12", "COPAS")
    assert jogo.verificar_carta_vencedora(Carta1, Carta2) == Carta2
    
def test_verificar_ganhador(jogo, interface, capsys):
    carta1 = Carta("1", "ESPADAS")
    carta2 = Carta("7", "OUROS")
    
    assert jogo.verificar_ganhador(carta1, carta2, interface) == carta1
    out, err = capsys.readouterr()
    assert out != ""
    
def test_adicionar_rodada(jogo, jogador1, jogador2):
    carta1 = Carta("1", "ESPADAS")
    carta2 = Carta("7", "OUROS")
    
    assert jogo.adicionar_rodada(jogador1, jogador2, carta1, carta2, carta1) == 1
    assert jogador1.rodadas == 1
    
    carta1 = Carta("1", "COPAS")
    carta2 = Carta("7", "OUROS")
    assert jogo.adicionar_rodada(jogador1, jogador2, carta1, carta2, carta2) == 2
    assert jogador2.rodadas == 1
    
    assert jogo.adicionar_rodada(jogador1, jogador2, carta1, carta2, "Empate") == "Erro"
    
def test_quem_joga_primeiro(jogo, jogador1, jogador2):
    carta1 = Carta("1", "ESPADAS")
    carta2 = Carta("7", "OUROS")
    
    try:
        jogo.quem_joga_primeiro(jogador1, jogador2, carta1, carta2, carta1)
    except:
        assert False
        
    assert jogador1.primeiro == True
    assert jogador2.primeiro == False
    
    carta1 = Carta("1", "COPAS")
    carta2 = Carta("7", "OUROS")
    
    try:
        jogo.quem_joga_primeiro(jogador1, jogador2, carta1, carta2, carta2)
    except:
        assert False
        
    assert jogador1.primeiro == False
    assert jogador2.primeiro == True
    
def test_quem_inicia_rodada(jogo, jogador1, jogador2):
    jogador1.rodadas = 0
    jogador2.rodadas = 0
    
    jogador1.ultimo = True
    try:
        jogo.quem_inicia_rodada(jogador1, jogador2)
    except:
        assert False
        
    assert jogador1.primeiro == True
    assert jogador2.primeiro == False
    assert jogador1.ultimo == False
    assert jogador2.ultimo == True
    
    jogador2.ultimo = True
    try:
        jogo.quem_inicia_rodada(jogador1, jogador2)
    except:
        assert False
        
    assert jogador2.primeiro == True
    assert jogador1.primeiro == False
    assert jogador2.ultimo == False
        
def test_jogador_fugiu(jogo, jogador1, jogador2, capsys):
    try:
        jogo.jogador_fugiu(None, jogador1, jogador2, 0)
    except:
        assert False
    
    assert jogador1.primeiro == True
    assert jogador2.primeiro == False
    
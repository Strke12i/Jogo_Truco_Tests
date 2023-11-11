from truco.jogador import Jogador
from truco.baralho import Baralho
from truco.carta import Carta
import pytest
import sys

@pytest.fixture
def jogador():
    return Jogador("Felipe")

@pytest.fixture
def cartas():
    return [Carta("1", "OUROS"), Carta("2", "ESPADAS"), Carta("3", "COPAS")]

def test_jogador(jogador):
    assert jogador.nome == "Felipe"
    assert jogador.mao == []
    assert jogador.mao_rank == []
    assert jogador.rodadas == 0
    assert jogador.pontos == 0
    assert jogador.envido == 0
    assert jogador.primeiro == False
    assert jogador.ultimo == False
    assert jogador.flor == False
    assert jogador.pediu_flor == False
    assert jogador.pediu_truco == False

def test_resetar(jogador):
    try:
        jogador.resetar()
        assert jogador.nome == "Felipe"
        assert jogador.mao == []
        assert jogador.pontos == 0
        assert jogador.flor == False
        assert jogador.pediu_truco == False
    except:
        assert False

def test_criar_mao(jogador):
    try:
        baralho = Baralho()
        baralho.criar_baralho()
        cartas = baralho.cartas[-3:]
        jogador.criar_mao(baralho)
    except:
        assert False     
    
    assert len(jogador.mao) == 3
    for i in range(0,3):
        assert cartas[i] == jogador.mao[2-i]

    envido = jogador.calcula_envido(jogador.mao)
    assert jogador.envido == envido

    
    
def test_jogar_carta(jogador, cartas):
    jogador.mao = cartas.copy()

    assert jogador.jogar_carta(0) == cartas[0]
    assert jogador.mao == [cartas[1], cartas[2]]
    assert jogador.jogar_carta(1) == cartas[2]
    assert jogador.mao == [cartas[1]]
    assert jogador.jogar_carta(0) == cartas[1]
    assert jogador.mao == []
    with pytest.raises(IndexError) as e_info:
        jogador.jogar_carta(0)
    
    assert str(e_info.value) == "pop from empty list"

def test_adicionar_pontos(jogador):
    pontos = 10
    jogador.adicionar_pontos(pontos)
    assert jogador.pontos == pontos

    jogador.adicionar_pontos(-pontos)
    assert jogador.pontos == 0

    jogador.adicionar_pontos(-pontos)
    assert jogador.pontos == -10

def test_mostrar_mao(jogador, cartas, capsys):
    jogador.mao = cartas.copy()
    jogador.mostrar_mao(None)
    out, err = capsys.readouterr()
    assert out == "[0] 1 de OUROS\n[1] 2 de ESPADAS\n[2] 3 de COPAS\n"

def test_checa_mao(jogador, cartas):
    jogador.mao = cartas.copy()
    assert jogador.checa_mao() == cartas

    jogador.mao = []
    assert jogador.checa_mao() == []

def test_adicionar_rodadas(jogador):
    jogador.adicionar_rodada()
    assert jogador.rodadas == 1

    jogador.adicionar_rodada()
    assert jogador.rodadas == 2

def test_retorna_pontos_envido(jogador):
    jogador.envido = 3
    assert jogador.retorna_pontos_envido() == 3

def test_checa_flor(jogador, cartas):
    jogador.mao = [Carta("1", "OUROS"), Carta("2", "OUROS"), Carta("3", "OUROS")]
    assert jogador.checa_flor() == True

    jogador.mao = cartas.copy()
    assert jogador.checa_flor() == False

def test_calcula_envido(jogador, cartas):
    jogador.mao = cartas.copy()
    assert jogador.calcula_envido(jogador.mao) == 3

    jogador.mao = [Carta("1", "OUROS"), Carta("2", "OUROS"), Carta("3", "OUROS")]
    assert jogador.calcula_envido(jogador.mao) == 25

def test_mostrar_opcoes(jogador, cartas, capsys):
    jogador.mao = cartas.copy()
    jogador.pediu_truco = False
    jogador.flor = False
    jogador.mostrar_opcoes(None)
    
    out, err = capsys.readouterr()
    assert out == "[0] 1 de OUROS\n[1] 2 de ESPADAS\n[2] 3 de COPAS\n[4] Truco\n[6] Envido\n[7] Real Envido\n[8] Falta Envido\n[9] Ir ao baralho\n"

    jogador.mao = [Carta("1", "OUROS"), Carta("2", "OUROS"), Carta("3", "OUROS")]
    jogador.pediu_truco = False
    jogador.mostrar_opcoes(None)

    out, err = capsys.readouterr()
    assert out == "[0] 1 de OUROS\n[1] 2 de OUROS\n[2] 3 de OUROS\n[4] Truco\n[5] Flor\n[6] Envido\n[7] Real Envido\n[8] Falta Envido\n[9] Ir ao baralho\n"

    
